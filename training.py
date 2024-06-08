import openai
import json

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Path to your training data file
file_path = 'path_to_your_training_data.jsonl'

# Function to upload a file to OpenAI
def upload_file(file_path):
    response = openai.File.create(
        file=open(file_path),
        purpose='fine-tune'
    )
    return response.id

# Function to create a fine-tuning job
def create_finetune(file_id):
    response = openai.FineTune.create(
        model="gpt-3.5-turbo",
        training_file=file_id,
        n_epochs=1,  # You can adjust epochs based on your needs
        learning_rate_multiplier=0.1,  # You can adjust the learning rate multiplier
        batch_size=4  # You can adjust the batch size
    )
    return response.id

# Function to get the status of a fine-tuning job
def get_finetune_status(job_id):
    response = openai.FineTune.retrieve(id=job_id)
    return response.status

# Main process
if __name__ == '__main__':
    # Upload your training file
    file_id = upload_file(file_path)
    print(f"Uploaded file ID: {file_id}")

    # Create fine-tuning job
    job_id = create_finetune(file_id)
    print(f"Fine-tuning job created with ID: {job_id}")

    # Optionally, check the status of the fine-tuning job
    status = get_finetune_status(job_id)
    print(f"Fine-tuning job status: {status}")
