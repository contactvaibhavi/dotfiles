#!/usr/bin/env python3
"""
Fully local RAG system - no API keys, no internet needed
Uses: sentence-transformers (embeddings) + Ollama (LLM)
"""

from pathlib import Path
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import subprocess
import sys


class LocalRAG:
    def __init__(self, collection_name="my_pdfs"):
        print("🔧 Initializing Local RAG...")

        # Load local embedding model (downloads on first run)
        print("📥 Loading embedding model (first time may take a minute)...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded")

        # Initialize local vector database
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")

        # Try to get existing collection or create new one
        try:
            self.collection = self.chroma_client.get_collection(collection_name)
            print(f"✅ Loaded existing collection: {collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(collection_name)
            print(f"✅ Created new collection: {collection_name}")

    def index_pdfs(self, folder_path, chunk_size=500, chunk_overlap=50):
        """Index all PDFs in a folder"""
        folder = Path(folder_path).expanduser()
        pdf_files = sorted(list(folder.glob("*.pdf")))

        if not pdf_files:
            print(f"❌ No PDFs found in {folder_path}")
            return

        print(f"\n📚 Indexing {len(pdf_files)} PDFs...")
        print(f"   Chunk size: {chunk_size} chars, overlap: {chunk_overlap}")
        print("")

        total_chunks = 0

        for pdf_file in pdf_files:
            try:
                with open(pdf_file, "rb") as file:
                    reader = PdfReader(file)
                    file_chunks = 0

                    for page_num, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if not text or len(text.strip()) < 50:
                            continue

                        # Create overlapping chunks
                        chunks = []
                        for i in range(0, len(text), chunk_size - chunk_overlap):
                            chunk = text[i : i + chunk_size]
                            if len(chunk.strip()) >= 50:
                                chunks.append(chunk)

                        # Add chunks to vector DB
                        for chunk_num, chunk in enumerate(chunks):
                            embedding = self.embedder.encode(chunk).tolist()

                            doc_id = f"{pdf_file.stem}_p{page_num + 1}_c{chunk_num}"

                            self.collection.add(
                                embeddings=[embedding],
                                documents=[chunk],
                                metadatas=[
                                    {
                                        "file": pdf_file.name,
                                        "page": page_num + 1,
                                        "chunk": chunk_num,
                                    }
                                ],
                                ids=[doc_id],
                            )

                            file_chunks += 1

                    total_chunks += file_chunks
                    print(f"✓ {pdf_file.name}: {file_chunks} chunks")

            except Exception as e:
                print(f"✗ Error indexing {pdf_file.name}: {e}")

        print(f"\n✅ Indexing complete! Total chunks: {total_chunks}")

    def query_ollama(self, prompt, model="llama3.1"):
        """Query local Ollama model"""
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "⚠️  Ollama took too long to respond. Try a simpler question."
        except FileNotFoundError:
            return "❌ Ollama not found. Install with: brew install ollama"

    def search(self, query, top_k=5):
        """Search for relevant chunks"""
        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        return results

    def ask(self, question, top_k=5, model="llama3.1", show_sources=True):
        """Ask a question and get an answer"""
        print(f"\n🔍 Searching knowledge base...")

        # Retrieve relevant chunks
        results = self.search(question, top_k)

        if not results["documents"][0]:
            print("❌ No relevant information found")
            return None

        # Build context from retrieved chunks
        context_parts = []
        for i, (doc, metadata) in enumerate(
            zip(results["documents"][0], results["metadatas"][0])
        ):
            context_parts.append(
                f"[Source {i + 1}: {metadata['file']}, Page {metadata['page']}]\n{doc}"
            )

        context = "\n\n".join(context_parts)

        # Show sources if requested
        if show_sources:
            print(f"\n📄 Found {len(results['documents'][0])} relevant chunks:")
            for metadata in results["metadatas"][0]:
                print(f"   • {metadata['file']} (Page {metadata['page']})")

        # Create prompt for LLM
        prompt = f"""Based on the following context from PDF documents, answer the question. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer:"""

        print(f"\n🤖 Generating answer with {model}...")

        # Get answer from Ollama
        answer = self.query_ollama(prompt, model)

        return answer, results


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Index PDFs:  python local_rag.py index <folder_path>")
        print("  Ask question: python local_rag.py ask '<question>'")
        print("  Interactive:  python local_rag.py interactive")
        print("\nExamples:")
        print("  python local_rag.py index ~/Documents/Textbooks")
        print("  python local_rag.py ask 'What is dynamic programming?'")
        print("  python local_rag.py interactive")
        sys.exit(1)

    command = sys.argv[1].lower()

    rag = LocalRAG()

    if command == "index":
        if len(sys.argv) < 3:
            print("❌ Please provide folder path")
            print("Usage: python local_rag.py index <folder_path>")
            sys.exit(1)

        folder = sys.argv[2]
        rag.index_pdfs(folder)

    elif command == "ask":
        if len(sys.argv) < 3:
            print("❌ Please provide a question")
            print("Usage: python local_rag.py ask '<question>'")
            sys.exit(1)

        question = sys.argv[2]
        answer, sources = rag.ask(question)

        print("\n" + "=" * 70)
        print("📝 ANSWER:")
        print("=" * 70)
        print(answer)
        print("=" * 70)

    elif command == "interactive":
        print("\n" + "=" * 70)
        print("🎯 Interactive RAG Mode")
        print("=" * 70)
        print("Type your questions (or 'quit' to exit)")
        print("")

        while True:
            try:
                question = input("\n💬 Question: ").strip()

                if question.lower() in ["quit", "exit", "q"]:
                    print("👋 Goodbye!")
                    break

                if not question:
                    continue

                answer, sources = rag.ask(question)

                print("\n" + "=" * 70)
                print("📝 ANSWER:")
                print("=" * 70)
                print(answer)
                print("=" * 70)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

    else:
        print(f"❌ Unknown command: {command}")
        print("Valid commands: index, ask, interactive")


if __name__ == "__main__":
    main()
