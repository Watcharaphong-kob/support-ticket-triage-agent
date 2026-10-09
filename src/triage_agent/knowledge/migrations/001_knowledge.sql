CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS kb_space (
    singleton integer PRIMARY KEY CHECK (singleton = 1),
    model text NOT NULL,
    dimension integer NOT NULL CHECK (dimension BETWEEN 1 AND 3072),
    index_version text NOT NULL
);
CREATE TABLE IF NOT EXISTS kb_documents (
    id text PRIMARY KEY,
    title text NOT NULL,
    locale text NOT NULL CHECK (locale IN ('en','th')),
    product text,
    issue_type text NOT NULL,
    version text NOT NULL,
    is_mock boolean NOT NULL,
    content_hash text NOT NULL
);
CREATE TABLE IF NOT EXISTS kb_chunks (
    id text PRIMARY KEY,
    document_id text NOT NULL REFERENCES kb_documents(id) ON DELETE CASCADE,
    sequence integer NOT NULL CHECK (sequence >= 0),
    text text NOT NULL,
    content_hash text NOT NULL,
    embedding vector NOT NULL,
    dimension integer NOT NULL CHECK (dimension BETWEEN 1 AND 3072),
    CHECK (vector_dims(embedding) = dimension),
    UNIQUE (document_id, sequence)
);
