class HealthController:
    @staticmethod
    async def get_health_status():
        return {
            "health": "i'm alive",
            "status": 200,
            "message": "ok"
        }
