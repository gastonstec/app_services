# app/routes/system.py
# This module defines system-related endpoints.

# Imports
from app.core.config import AppSettings
# FastAPI imports
from fastapi import APIRouter, HTTPException, Request


# Create FastAPI router for system-related endpoints
router = APIRouter()


# Health check
@router.get("/api/v1/sys/health", summary="Health Check")
async def health_check():
    return {
        'App Name': AppSettings.name,
        'Version': AppSettings.version,
        'Description': AppSettings.description
    }


# Get database version
@router.get("/api/v1/sys/dbver", summary="Get Database Version")
async def get_db_version(request: Request):
    # Get the database version
    try:
        db_version = request.app.state.db_conn.test()
        if db_version is None:
            raise HTTPException(
                status_code=404,
                detail="Database version not found"
            )
            return
        return {"db_version": db_version}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving database version: {str(e)}"
        )


# Get database stats
@router.get("/api/v1/sys/dbinfo", summary="Get Database connection Stats")
async def get_db_conn_info(request: Request):
    # Get the database connection pool from the app state
    pool = request.app.state.db_conn.pool
    return {"connection_stats": str(pool.get_stats())}
