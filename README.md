# Design Docs for Info 253b project

## Build and Run
### 1. Database container
```
cd database
chmod +x setup.sh
./setup.sh
```

```
We need to run each command in the file `initialize_db` to seed the db
```
### 2. Dcouments APIs
```
cd documents
chmod +x setup.sh
./setup.sh
```
### 3. Folder APIs
```
TODO
```

## Documents API
### 1. Create a new document
```json
POST /v1/documents/
```
#### Input
```
{
    "title": 
    "content":
    "folder_id": optional
}
```
#### Output
```
{
    "id": 1
}
```
### 2. Get a document content
```
GET /v1/documents/<id>
```
#### Output
```
{
    "id":
    "title":
    "text":
}
```
### 3. Get a spell check for a document
```
GET /v1/documents/<id>/spell_check
(Calls external API)
```
#### Output
```
{
    "id":
    "text":
    "spell_check": 
}
```

### 4. Word counts
```
GET /v1/documents/<id>/word_count/<stop_word>
```
#### Input
```json
{
    "stop_word": 0 for false, 1 for true
}
```
#### Output
```json
{
    "id":
    "word_count": []
}
```

### 5. Change document
```
PUT /v1/documents/<id>
```

#### Input
```json
{
    "title": optional
    "text": optional
    "folder_id": optional
}
```
#### Output
```json
{
    success
}
```
### 6. Delete document

```
DELETE /v1/documents/<id>
```
#### Output
```json
Success
```

### 7. Get multiple documents
```
GET /v1/documents/
```
#### Input
```json
    "id": [id1, id2]
```

#### Output
```json
    "result": [
    {
    "title": optional
    "text": optional
    "folder_id": optional
    },
    {
    "title": optional
    "text": optional
    "folder_id": optional
    }
    ]
```


## Folders API
### 1. Create a folder
```json
POST /v1/folders/
```
#### Input
```json
    "name":
```
#### Output
```json
    "id": 
```

### 2. Add a documents to folder
```json
    POST /v1/folders/<id>/add_document
```
#### Input
```
{
    "document_id": 
}
```
#### Output
```
{
    Success
}
```

### 3. List all documents in a folder
```
GET /v1/folders/<id>
```
#### Output
```
{
    
    document_ids: [id1, id2, id3]
}
```

### 4. Edit folders
```
PUT /v1/folders/<id>
```
#### Input
```
    "name": 
```
#### Output 
```
    Success
```
### 5. Delete folder
```
DELETE /v1/folders/<id>
```
#### Output
```
Success
```

### 6. Get all folders
```
GET /v1/folders/
```
#### Output
```json
{
    result: [
        {
        "name": 
        "id": 
        },
        {
        "name": 
        "id":
        }
    ]
}
```

## Database Schema
### Documents Schema

| id (primary)  | title    | content  | last_modified| 
| ------------- | -------- | -------- | --------     |
| int (auto inc)| Text     | Text     |              |

### Folders Schema
| id (primary) | title|
| ------------ | -----|
|int (auto inc)| Text |

### Folder-Document Schema
| folder_id    | document_id |
| -----------  | ----------- |
| int          | int         |
