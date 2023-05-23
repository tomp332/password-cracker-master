import uvicorn

from password_cracker_master import master_context

if __name__ == "__main__":
    uvicorn.run("password_cracker_master.src.server:main_api_router", host=master_context.main_settings.framework_hostname,
                port=master_context.main_settings.framework_port)
