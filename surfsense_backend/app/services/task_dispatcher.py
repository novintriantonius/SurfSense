"""Task dispatcher abstraction for background document processing.

Decouples the upload endpoint from Celery so tests can swap in a
synchronous (inline) implementation that needs only PostgreSQL.
"""

from __future__ import annotations

from typing import Protocol


class TaskDispatcher(Protocol):
    async def dispatch_file_processing(
        self,
        *,
        document_id: int,
        temp_path: str,
        filename: str,
        search_space_id: int,
        user_id: str,
        use_vision_llm: bool = False,
        processing_mode: str = "basic",
    ) -> None: ...

    async def dispatch_uploaded_folder_processing(
        self,
        *,
        search_space_id: int,
        user_id: str,
        folder_name: str,
        root_folder_id: int | None,
        file_mappings: list[dict],
        use_vision_llm: bool = False,
        processing_mode: str = "basic",
    ) -> None:
        """Process folder upload files asynchronously."""
        pass

class CeleryTaskDispatcher:
    """Production dispatcher — fires Celery tasks via Redis broker."""

    async def dispatch_file_processing(
        self,
        *,
        document_id: int,
        temp_path: str,
        filename: str,
        search_space_id: int,
        user_id: str,
        use_vision_llm: bool = False,
        processing_mode: str = "basic",
    ) -> None:
        from app.tasks.celery_tasks.document_tasks import (
            process_file_upload_with_document_task,
        )

        process_file_upload_with_document_task.delay(
            document_id=document_id,
            temp_path=temp_path,
            filename=filename,
            search_space_id=search_space_id,
            user_id=user_id,
            use_vision_llm=use_vision_llm,
            processing_mode=processing_mode,
        )

    async def dispatch_uploaded_folder_processing(
        self,
        *,
        search_space_id: int,
        user_id: str,
        folder_name: str,
        root_folder_id: int | None,
        file_mappings: list[dict],
        use_vision_llm: bool = False,
        processing_mode: str = "basic",
    ) -> None:
        from app.tasks.celery_tasks.document_tasks import (
            index_uploaded_folder_files_task,
        )

        index_uploaded_folder_files_task.delay(
            search_space_id=search_space_id,
            user_id=user_id,
            folder_name=folder_name,
            root_folder_id=root_folder_id,
            use_vision_llm=use_vision_llm,
            file_mappings=file_mappings,
            processing_mode=processing_mode,
        )


async def get_task_dispatcher() -> TaskDispatcher:
    return CeleryTaskDispatcher()
