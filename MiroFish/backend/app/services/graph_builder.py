"""
图谱构建服务
接口2：使用 Redis 构建和存储图谱
"""

import asyncio
import json
import threading
import uuid
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

from ..models.task import TaskManager, TaskStatus
from ..utils.redis_client import redis_db
from .text_processor import TextProcessor
from ..utils.locale import t, get_locale, set_locale


@dataclass
class GraphInfo:
    """图谱信息"""
    graph_id: str
    node_count: int
    edge_count: int
    entity_types: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "entity_types": self.entity_types,
        }


async def build_initial_graph(agent_id: str, extracted_entities: list, extracted_edges: list):
    """
    Replaces Zep's builder.set_ontology.
    Saves nodes and edges to Redis Hashes.
    """
    nodes_key = f"mirofish:{agent_id}:nodes"
    edges_key = f"mirofish:{agent_id}:edges"

    if extracted_entities:
        node_mapping = {
            entity["name"]: json.dumps(entity, ensure_ascii=False)
            for entity in extracted_entities
            if entity.get("name")
        }
        if node_mapping:
            await redis_db.hset(nodes_key, mapping=node_mapping)

    if extracted_edges:
        edge_mapping = {
            f"{edge['source']}->{edge['target']}": json.dumps(edge, ensure_ascii=False)
            for edge in extracted_edges
            if edge.get("source") and edge.get("target")
        }
        if edge_mapping:
            await redis_db.hset(edges_key, mapping=edge_mapping)

    print(f"Graph built in Redis for agent {agent_id}")


class GraphBuilderService:
    """
    图谱构建服务
    负责构建并持久化知识图谱到 Redis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.task_manager = TaskManager()
    
    def build_graph_async(
        self,
        text: str,
        ontology: Dict[str, Any],
        graph_name: str = "MiroFish Graph",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        batch_size: int = 3
    ) -> str:
        """
        异步构建图谱
        
        Args:
            text: 输入文本
            ontology: 本体定义（来自接口1的输出）
            graph_name: 图谱名称
            chunk_size: 文本块大小
            chunk_overlap: 块重叠大小
            batch_size: 每批发送的块数量
            
        Returns:
            任务ID
        """
        # 创建任务
        task_id = self.task_manager.create_task(
            task_type="graph_build",
            metadata={
                "graph_name": graph_name,
                "chunk_size": chunk_size,
                "text_length": len(text),
            }
        )
        
        # Capture locale before spawning background thread
        current_locale = get_locale()

        # 在后台线程中执行构建
        thread = threading.Thread(
            target=self._build_graph_worker,
            args=(task_id, text, ontology, graph_name, chunk_size, chunk_overlap, batch_size, current_locale)
        )
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def _build_graph_worker(
        self,
        task_id: str,
        text: str,
        ontology: Dict[str, Any],
        graph_name: str,
        chunk_size: int,
        chunk_overlap: int,
        batch_size: int,
        locale: str = 'zh'
    ):
        """图谱构建工作线程"""
        set_locale(locale)
        try:
            self.task_manager.update_task(
                task_id,
                status=TaskStatus.PROCESSING,
                progress=5,
                message=t('progress.startBuildingGraph')
            )
            
            # 1. 创建图谱标识
            graph_id = self.create_graph(graph_name)
            self.task_manager.update_task(
                task_id,
                progress=10,
                message=t('progress.graphCreated', graphId=graph_id)
            )
            
            # 2. 设置本体并写入 Redis
            self.set_ontology(graph_id, ontology)
            self.task_manager.update_task(
                task_id,
                progress=15,
                message=t('progress.ontologySet')
            )
            
            # 3. 文本分块（保留原有统计信息）
            chunks = TextProcessor.split_text(text, chunk_size, chunk_overlap)
            total_chunks = len(chunks)
            self.task_manager.update_task(
                task_id,
                progress=20,
                message=t('progress.textSplit', count=total_chunks)
            )

            # 4. 获取图谱信息
            self.task_manager.update_task(
                task_id,
                progress=90,
                message=t('progress.fetchingGraphInfo')
            )
            
            graph_info = self._get_graph_info(graph_id)
            
            # 完成
            self.task_manager.complete_task(task_id, {
                "graph_id": graph_id,
                "graph_info": graph_info.to_dict(),
                "chunks_processed": total_chunks,
            })
            
        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.task_manager.fail_task(task_id, error_msg)
    
    def create_graph(self, name: str) -> str:
        """创建图谱标识（公开方法）"""
        graph_id = f"mirofish_{uuid.uuid4().hex[:16]}"
        return graph_id
    
    def set_ontology(self, graph_id: str, ontology: Dict[str, Any]):
        """设置图谱本体（公开方法）"""
        extracted_entities, extracted_edges = self._ontology_to_redis_payload(ontology)
        self._run_async(build_initial_graph(graph_id, extracted_entities, extracted_edges))

    def _run_async(self, coroutine):
        """在同步上下文中执行异步 Redis 操作。"""
        asyncio.run(coroutine)

    def _ontology_to_redis_payload(self, ontology: Dict[str, Any]) -> tuple[list, list]:
        extracted_entities = []
        for entity_def in ontology.get("entity_types", []):
            extracted_entities.append({
                "name": entity_def.get("name"),
                "description": entity_def.get("description"),
                "attributes": entity_def.get("attributes", []),
                "examples": entity_def.get("examples", []),
            })

        extracted_edges = []
        for edge_def in ontology.get("edge_types", []):
            for source_target in edge_def.get("source_targets", []):
                source = source_target.get("source")
                target = source_target.get("target")
                if not source or not target:
                    continue

                extracted_edges.append({
                    "name": edge_def.get("name"),
                    "source": source,
                    "target": target,
                    "description": edge_def.get("description"),
                    "attributes": edge_def.get("attributes", []),
                })

        return extracted_entities, extracted_edges
    
    def add_text_batches(
        self,
        graph_id: str,
        chunks: List[str],
        batch_size: int = 3,
        progress_callback: Optional[Callable] = None
    ) -> List[str]:
        """保留兼容接口；Redis 实现不再分批发送文本。"""
        if progress_callback and chunks:
            progress_callback(
                t('progress.sendingBatch', current=1, total=1, chunks=len(chunks)),
                1.0
            )
        return []
    
    def _wait_for_episodes(
        self,
        episode_uuids: List[str],
        progress_callback: Optional[Callable] = None,
        timeout: int = 600
    ):
        """保留兼容接口；Redis 实现不再等待 Zep 处理。"""
        if progress_callback:
            progress_callback(t('progress.processingComplete', completed=0, total=0), 1.0)
    
    def _get_graph_info(self, graph_id: str) -> GraphInfo:
        """从 Redis 获取图谱信息"""
        nodes_key = f"mirofish:{graph_id}:nodes"
        edges_key = f"mirofish:{graph_id}:edges"

        nodes_data = asyncio.run(redis_db.hgetall(nodes_key))
        edges_data = asyncio.run(redis_db.hgetall(edges_key))

        entity_types = sorted(list(nodes_data.keys()))

        return GraphInfo(
            graph_id=graph_id,
            node_count=len(nodes_data),
            edge_count=len(edges_data),
            entity_types=entity_types,
        )
    
    def get_graph_data(self, graph_id: str) -> Dict[str, Any]:
        """
        获取完整图谱数据（包含详细信息）
        
        Args:
            graph_id: 图谱ID
            
        Returns:
            包含nodes和edges的字典，包括时间信息、属性等详细数据
        """
        nodes_key = f"mirofish:{graph_id}:nodes"
        edges_key = f"mirofish:{graph_id}:edges"

        nodes_raw = asyncio.run(redis_db.hgetall(nodes_key))
        edges_raw = asyncio.run(redis_db.hgetall(edges_key))

        nodes_data = []
        for node_name, node_json in nodes_raw.items():
            node_data = json.loads(node_json)
            nodes_data.append({
                "uuid": node_name,
                "name": node_data.get("name", node_name),
                "labels": [node_data.get("name", node_name)],
                "summary": node_data.get("description", ""),
                "attributes": node_data.get("attributes", []),
                "created_at": None,
            })

        edges_data = []
        for edge_key, edge_json in edges_raw.items():
            edge_data = json.loads(edge_json)
            source = edge_data.get("source", "")
            target = edge_data.get("target", "")
            edges_data.append({
                "uuid": edge_key,
                "name": edge_data.get("name", ""),
                "fact": edge_data.get("description", ""),
                "fact_type": edge_data.get("name", ""),
                "source_node_uuid": source,
                "target_node_uuid": target,
                "source_node_name": source,
                "target_node_name": target,
                "attributes": edge_data.get("attributes", []),
                "created_at": None,
                "valid_at": None,
                "invalid_at": None,
                "expired_at": None,
                "episodes": [],
            })
        
        return {
            "graph_id": graph_id,
            "nodes": nodes_data,
            "edges": edges_data,
            "node_count": len(nodes_data),
            "edge_count": len(edges_data),
        }
    
    def delete_graph(self, graph_id: str):
        """删除图谱"""
        nodes_key = f"mirofish:{graph_id}:nodes"
        edges_key = f"mirofish:{graph_id}:edges"
        asyncio.run(redis_db.delete(nodes_key, edges_key))

