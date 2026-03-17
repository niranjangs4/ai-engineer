import numpy as np
from sentence_transformers import SentenceTransformer


class RAGMemory:

    def __init__(self):

        # embedding model
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # in-memory vector store
        self.data = []

    ############################################################
    # ADD MEMORY
    ############################################################

    def add(self, text, metadata):

        emb = self.model.encode(text, normalize_embeddings=True)
        # 🔥 DEDUP CHECK
        for item in self.data:
            if (
                    item["metadata"].get("selector") == metadata.get("selector")
                    and item["metadata"].get("action") == metadata.get("action")
                    and item["metadata"].get("page") == metadata.get("page")
            ):
                item["confidence"] = min(item.get("confidence", 0.5) + 0.1, 1.0)
                print("📈 Boosting selector confidence")
                return

        # store new
        self.data.append({
            "embedding": emb,
            "text": text,
            "metadata": metadata,
            "confidence": 0.5
        })

    ############################################################
    # SEARCH MEMORY
    ############################################################
    def search(self, query, k=3):

        if not self.data:
            return []

        q = self.model.encode(query, normalize_embeddings=True)

        scores = []

        for item in self.data:

            if item["metadata"].get("type") != "selector":
                continue

            emb = item["embedding"]

            sim = float(np.dot(q, emb)) * item.get("confidence", 0.5)
            if sim < 0.3:
                continue

            scores.append({
                "score": sim,
                "item": item
            })

        scores = sorted(scores, key=lambda x: x["score"], reverse=True)

        # 🔥 fallback if nothing passes threshold
        if not scores:
            fallback = [
                item for item in self.data
                if item["metadata"].get("type") == "selector"
            ]

            if fallback:
                return fallback[:k]

            return self.data[:k]  # 🔥 ultimate fallback

        return [x["item"] for x in scores[:k]]

    ############################################################
    # SETUP INITIAL RAG KNOWLEDGE
    ############################################################

    def setup_rag(self):

        # Zodiac login workflow knowledge
        self.add(

            text="Accept the cookie banner by clicking the 'Accept All Cookies' button",

            metadata={

                "type": "selector",

                "application": "zodiac",

                "page": "login",

                "action": "accept_cookie",

                "selector": "div.overlay-content button:has-text('Accept All Cookies')"

            }

        )
        self.add(

            text="zodiac login workflow accept cookies enter username enter password click sign in",

            metadata={

                "type": "workflow",
                "application": "zodiac",
                "page": "login",
                "username": "username",
                "password": "password",
                "url":"https://zodiacappqp.zv8.zodiac-cloud.com/zodiac/ui/auth",
                "steps": [

                    "open application url",
                    "accept cookie banner",
                    "enter username",
                    "enter password",
                    "click sign in",
                    "Verify homepage menu is visible"

                ]

            }

        )
        self.add(

            text="after successful login the user avatar icon appears in the header",

            metadata={

                "type": "selector",
                "application": "zodiac",
                "page": "homepage",
                "action": "login_success_indicator",

                "selector": ".user-avatar"

            }

        )
        # cookie banner knowledge

        self.add(

            text="cookie banner must be accepted before login",

            metadata={

                "type": "workflow",
                "application": "zodiac",
                "page": "login",

                "steps": [

                    "click Accept All Cookies button"

                ]

            }

        )

        # login UI pattern knowledge

        # self.add(
        #
        #     text="login form contains username password and sign in button",
        #
        #     metadata={
        #
        #         "type": "ui_pattern",
        #
        #         "elements": [
        #
        #             "username input",
        #             "password input",
        #             "sign in button"
        #
        #         ]
        #
        #     }
        #
        # )

        print("RAG knowledge initialized")