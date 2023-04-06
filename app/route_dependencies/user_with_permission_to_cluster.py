from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth import current_active_user
from auth.models import User
from repositories import TaxonomyDatabaseRepository, UserRepository
from route_dependencies import get_db


def user_with_permission_to_cluster(
    cluster_id: int,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(current_active_user)
):
    taxonomy_repo = TaxonomyDatabaseRepository(db)
    taxonomy = taxonomy_repo.get()

    user_repo = UserRepository(db)
    user = user_repo.get(current_active_user.id)
    if not user.has_access_to_cluster(cluster_id, taxonomy):
        raise HTTPException(400, f"You dont have permission to edit this cluster")

    return current_active_user
