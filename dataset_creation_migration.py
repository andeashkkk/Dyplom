import os
import json

def read_annotations(annotation_file):
    annotations = []
    with open(annotation_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('T'):
                parts = line.strip().split()
                tag = parts[1]
                entity = ' '.join(parts[2:])
                annotations.append((entity, tag))
    return annotations

def process_files(text_folder, annotation_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        for filename in os.listdir(text_folder):
            if filename.endswith('.txt'):
                text_path = os.path.join(text_folder, filename)
                annotation_path = os.path.join(annotation_folder, filename.replace('.txt', '.ann'))
                
                with open(text_path, 'r', encoding='utf-8') as text_file:
                    text_content = text_file.read()
                    sentences = text_content.split('.')  # Simple sentence splitting

                    for sentence in sentences:
                        prompt = sentence.strip() + '\n\n###\n\n'
                        if os.path.exists(annotation_path):
                            annotations = read_annotations(annotation_path)
                            sentence_annotations = []
                            for entity, tag in annotations:
                                if entity in sentence:
                                    sentence_annotations.append(f"('{entity}', '{tag}')")
                            completion = '\n'.join(sentence_annotations) if sentence_annotations else 'NONE'
                        else:
                            completion = 'NONE'
                        
                        json_line = {
                            'prompt': prompt,
                            'completion': completion + ' END'
                        }
                        jsonl_file.write(json.dumps(json_line) + '\n')

def migrate(jsonl_file_path, new_jsonl_file_path):
    with open(jsonl_file_path, 'r', encoding='utf-8') as file, open(new_jsonl_file_path, 'w', encoding='utf-8') as new_file:
        for line in file:
            data = json.loads(line)
            prompt = data['prompt'].split('\n\n###\n\n')[0].strip()
            completion = data['completion'].replace(' END', '').strip()
            new_format = {
                "messages": [
                    {"role": "system", "content": "You are NERtagger, an expert bot designed to perform NER tagging accurately."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            }
            new_file.write(json.dumps(new_format) + '\n')

# Example usage:
process_files('path/to/text_folder', 'path/to/annotation_folder', 'output.jsonl')
migrate('output.jsonl', 'migrated_output.jsonl')
