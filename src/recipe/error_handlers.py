

async def create_error(e):
    return {
        "error": "error",
        "status": 500,
        "msg": e,
    }


async def create_integrity_error(e):
    return {
        "error": "error",
        "desc": "integrity_error",
        "status": 500,
        "msg": e.orig,
    }
