# Step 1: Build a Docker image named "virtu_gpt" using the current directory (.) as the build context.
docker build -t virtu_gpt .

# Step 2: Create Docker volumes for storing models and source documents.
# # These volumes will persist data even after containers are removed.
docker volume create models
docker volume create source_documents

# Step 3: Run a Docker container from the "virtu_gpt" image in detached mode (-d).
# Mount the "models" volume to the "/usr/src/app/models" directory inside the container,
# and mount the "source_documents" volume to the "/usr/src/app/source_documents" directory.
docker run --name virtu_gpt -p 8501:8501 -d -v models:/usr/src/app/models -v source_documents:/usr/src/app/source_documents virtu_gpt

# Logging: Print a message indicating the Docker setup is complete.
# echo "Docker setup is complete. Container is running with models and source documents volumes."
