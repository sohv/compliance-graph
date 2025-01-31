from llmsherpa.readers import LayoutPDFReader
from neo4j import GraphDatabase
import uuid
import hashlib
import os
import glob
from datetime import datetime
import time
from dotenv import load_dotenv

path = "/Users/sohan/Desktop/rag/.env"
load_dotenv(path)

NEO4J_URL = os.environ["NEO4J_URI"]
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
NEO4J_DATABASE = "neo4j"

file_location = '/Users/sohan/Desktop/rag/output'

# initialize Neo4j
def initialiseNeo4j():
    cypher_schema = [
        "CREATE CONSTRAINT sectionKey IF NOT EXISTS FOR (c:Section) REQUIRE (c.key) IS UNIQUE;",
        "CREATE CONSTRAINT chunkKey IF NOT EXISTS FOR (c:Chunk) REQUIRE (c.key) IS UNIQUE;",
        "CREATE CONSTRAINT documentKey IF NOT EXISTS FOR (c:Document) REQUIRE (c.url_hash) IS UNIQUE;",
        "CREATE CONSTRAINT tableKey IF NOT EXISTS FOR (c:Table) REQUIRE (c.key) IS UNIQUE;",
        "CALL db.index.vector.createNodeIndex('chunkVectorIndex', 'Embedding', 'value', 1536, 'COSINE');"
    ]
    
    driver = GraphDatabase.driver(NEO4J_URL, database=NEO4J_DATABASE, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        for cypher in cypher_schema:
            session.run(cypher)
    driver.close()

def ingestDocumentNeo4j(doc, doc_location):
    cypher_pool = [
        "MERGE (d:Document {name: $doc_name_val}) ON CREATE SET d.url = $doc_url_val RETURN d;",
        "MERGE (p:Section {key: $doc_name_val+'|'+$block_idx_val+'|'+$title_hash_val}) ON CREATE SET p.page_idx = $page_idx_val, p.title_hash = $title_hash_val, p.block_idx = $block_idx_val, p.title = $title_val, p.tag = $tag_val, p.level = $level_val RETURN p;",
        "MATCH (d:Document {name: $doc_name_val}) MATCH (s:Section {key: $doc_name_val+'|'+$block_idx_val+'|'+$title_hash_val}) MERGE (d)<-[:HAS_DOCUMENT]-(s);",
        "MATCH (s1:Section {key: $doc_name_val+'|'+$parent_block_idx_val+'|'+$parent_title_hash_val}) MATCH (s2:Section {key: $doc_name_val+'|'+$block_idx_val+'|'+$title_hash_val}) MERGE (s1)<-[:UNDER_SECTION]-(s2);",
        "MERGE (c:Chunk {key: $doc_name_val+'|'+$block_idx_val+'|'+$sentences_hash_val}) ON CREATE SET c.sentences = $sentences_val, c.sentences_hash = $sentences_hash_val, c.block_idx = $block_idx_val, c.page_idx = $page_idx_val, c.tag = $tag_val, c.level = $level_val RETURN c;",
        "MATCH (c:Chunk {key: $doc_name_val+'|'+$block_idx_val+'|'+$sentences_hash_val}) MATCH (s:Section {key:$doc_name_val+'|'+$parent_block_idx_val+'|'+$parent_hash_val}) MERGE (s)<-[:HAS_PARENT]-(c);",
        "MERGE (t:Table {key: $doc_name_val+'|'+$block_idx_val+'|'+$name_val}) ON CREATE SET t.name = $name_val, t.doc_name = $doc_name_val, t.block_idx = $block_idx_val, t.page_idx = $page_idx_val, t.html = $html_val, t.rows = $rows_val RETURN t;",
        "MATCH (t:Table {key: $doc_name_val+'|'+$block_idx_val+'|'+$name_val}) MATCH (s:Section {key: $doc_name_val+'|'+$parent_block_idx_val+'|'+$parent_hash_val}) MERGE (s)<-[:HAS_PARENT]-(t);",
        "MATCH (t:Table {key: $doc_name_val+'|'+$block_idx_val+'|'+$name_val}) MATCH (s:Document {name: $doc_name_val}) MERGE (s)<-[:HAS_PARENT]-(t);"
    ]

    driver = GraphDatabase.driver(NEO4J_URL, database=NEO4J_DATABASE, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        doc_name_val = os.path.basename(doc_location)
        doc_url_val = doc_location
        cypher = cypher_pool[0]
        session.run(cypher, doc_name_val=doc_name_val, doc_url_val=doc_url_val)

        for sec in doc.sections():
            sec_title_val = sec.title
            sec_title_hash_val = hashlib.md5(sec_title_val.encode("utf-8")).hexdigest()
            sec_tag_val = sec.tag
            sec_level_val = sec.level
            sec_page_idx_val = sec.page_idx
            sec_block_idx_val = sec.block_idx

            if sec_tag_val != 'table':
                cypher = cypher_pool[1]
                session.run(cypher, page_idx_val=sec_page_idx_val, title_hash_val=sec_title_hash_val, title_val=sec_title_val, tag_val=sec_tag_val, level_val=sec_level_val, block_idx_val=sec_block_idx_val, doc_name_val=doc_name_val)

                sec_parent_val = str(sec.parent.to_text())
                if sec_parent_val == "None":
                    cypher = cypher_pool[2]
                    session.run(cypher, page_idx_val=sec_page_idx_val, title_hash_val=sec_title_hash_val, doc_name_val=doc_name_val, block_idx_val=sec_block_idx_val)
                else:
                    sec_parent_title_hash_val = hashlib.md5(sec_parent_val.encode("utf-8")).hexdigest()
                    sec_parent_page_idx_val = sec.parent.page_idx
                    sec_parent_block_idx_val = sec.parent.block_idx
                    cypher = cypher_pool[3]
                    session.run(cypher, page_idx_val=sec_page_idx_val, title_hash_val=sec_title_hash_val, block_idx_val=sec_block_idx_val, parent_page_idx_val=sec_parent_page_idx_val, parent_title_hash_val=sec_parent_title_hash_val, parent_block_idx_val=sec_parent_block_idx_val, doc_name_val=doc_name_val)

        for chk in doc.chunks():
            chunk_block_idx_val = chk.block_idx
            chunk_page_idx_val = chk.page_idx
            chunk_tag_val = chk.tag
            chunk_level_val = chk.level
            chunk_sentences = "\n".join(chk.sentences)

            if chunk_tag_val != 'table':
                chunk_sentences_hash_val = hashlib.md5(chunk_sentences.encode("utf-8")).hexdigest()
                cypher = cypher_pool[4]
                session.run(cypher, sentences_hash_val=chunk_sentences_hash_val, sentences_val=chunk_sentences, block_idx_val=chunk_block_idx_val, page_idx_val=chunk_page_idx_val, tag_val=chunk_tag_val, level_val=chunk_level_val, doc_name_val=doc_name_val)

                chk_parent_val = str(chk.parent.to_text())
                if chk_parent_val != "None":
                    chk_parent_hash_val = hashlib.md5(chk_parent_val.encode("utf-8")).hexdigest()
                    chk_parent_page_idx_val = chk.parent.page_idx
                    chk_parent_block_idx_val = chk.parent.block_idx
                    cypher = cypher_pool[5]
                    session.run(cypher, sentences_hash_val=chunk_sentences_hash_val, block_idx_val=chunk_block_idx_val, parent_hash_val=chk_parent_hash_val, parent_block_idx_val=chk_parent_block_idx_val, doc_name_val=doc_name_val)

        for tb in doc.tables():
            page_idx_val = tb.page_idx
            block_idx_val = tb.block_idx
            name_val = 'block#' + str(block_idx_val) + '_' + tb.name
            html_val = tb.to_html()
            rows_val = len(tb.rows)
            cypher = cypher_pool[6]
            session.run(cypher, block_idx_val=block_idx_val, page_idx_val=page_idx_val, name_val=name_val, html_val=html_val, rows_val=rows_val, doc_name_val=doc_name_val)

            table_parent_val = str(tb.parent.to_text())
            if table_parent_val != "None":
                table_parent_hash_val = hashlib.md5(table_parent_val.encode("utf-8")).hexdigest()
                table_parent_page_idx_val = tb.parent.page_idx
                table_parent_block_idx_val = tb.parent.block_idx
                cypher = cypher_pool[7]
                session.run(cypher, name_val=name_val, block_idx_val=block_idx_val, parent_page_idx_val=table_parent_page_idx_val, parent_hash_val=table_parent_hash_val, parent_block_idx_val=table_parent_block_idx_val, doc_name_val=doc_name_val)
            else:
                cypher = cypher_pool[8]
                session.run(cypher, name_val=name_val, block_idx_val=block_idx_val, doc_name_val=doc_name_val)

        print(f'\'{doc_name_val}\' Done! Summary: ')
        print('#Sections: ' + str(len(doc.sections())))
        print('#Chunks: ' + str(len(doc.chunks())))
        print('#Tables: ' + str(len(doc.tables())))

    driver.close()

# Parse PDFs and ingest into Neo4j
def parseAndIngestPDFs():
    pdf_files = glob.glob(file_location + '/*.pdf')
    print(f'#PDF files found: {len(pdf_files)}!')

    pdf_reader = LayoutPDFReader("https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all")

    startTime = datetime.now()

    for pdf_file in pdf_files:
        doc = pdf_reader.read_pdf(pdf_file)
        ingestDocumentNeo4j(doc, pdf_file)

    print(f'Total time: {datetime.now() - startTime}')

# Initialize Neo4j
initialiseNeo4j()

# Parse PDFs and ingest into Neo4j
parseAndIngestPDFs()