from ..base import *


@app.get('/api/opportunity-provider/logo/{provider_id}')
async def get_opportunity_provider_logo(provider_id: Annotated[int, Path(ge=1)]):
    class ErrorCode(IntEnum):
        INVALID_PROVIDER_ID = 200

    with db.Session.begin() as session:
        provider = mw.get_opportunity_provider_by_id(
            session, provider_id, error_code=ErrorCode.INVALID_PROVIDER_ID
        )
        if not isinstance(provider, db.OpportunityProvider):
            return JSONResponse(provider, status_code=422)
        return Response(provider.get_logo(db.minio_client))
