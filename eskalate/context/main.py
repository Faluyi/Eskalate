from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from eskalate.api.applicant.router import router as applicants_router
from eskalate.api.application.router import router as applications_router
from eskalate.api.company.router import router as companies_router
from eskalate.api.job.router import router as jobs_router
from eskalate.api.auth.router import router as auth_router


app = FastAPI(
    title="Job Portal API",
    version="1.0.0",
    description="API for job applications, companies, applicants, and authentication"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
app.include_router(companies_router, prefix="/companies", tags=["Companies"])
app.include_router(applicants_router, prefix="/applicants", tags=["Applicants"])
app.include_router(applications_router, prefix="/applications", tags=["Applications"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Job Portal API"}
