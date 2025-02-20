# app.py
import streamlit as st
from typing import Dict, List, Optional

class FintechChatbot:
    # [Previous FintechChatbot class implementation remains the same]
    def __init__(self):
        self.knowledge_base = {
            "loan": {
                "definition": "A sum of money borrowed that is expected to be paid back with interest",
                "types": ["Personal Loan", "Home Loan", "Business Loan", "Education Loan"],
                "key_terms": ["EMI", "Interest Rate", "Tenure", "Principal Amount"]
            },
            "credit_score": {
                "definition": "A numerical expression of creditworthiness based on credit history",
                "range": "300-900",
                "providers": ["CIBIL", "Experian", "Equifax"],
                "factors": ["Payment History", "Credit Utilization", "Credit Age", "Credit Mix"]
            },
            "interest_rate": {
                "definition": "The percentage of principal charged by lender for loan use",
                "types": ["Fixed Rate", "Floating Rate", "Base Rate", "MCLR"],
                "factors": ["RBI Policy", "Credit Score", "Market Conditions", "Loan Type"]
            }
        }

        self.query_patterns = {
            "loan_types": ["what types of loans", "loan options", "different loans"],
            "credit_score_info": ["what is credit score", "cibil score", "credit rating"],
            "interest_rates": ["interest rates", "rate of interest", "how much interest"]
        }

    def preprocess_query(self, query: str) -> str:
        return query.lower().strip()

    def identify_intent(self, query: str) -> str:
        query = self.preprocess_query(query)
        
        for intent, patterns in self.query_patterns.items():
            if any(pattern in query for pattern in patterns):
                return intent
                
        for topic in self.knowledge_base.keys():
            if topic.replace("_", " ") in query:
                return topic
                
        return "unknown"

    def get_response(self, query: str) -> Dict:
        intent = self.identify_intent(query)
        response = {
            "text": "",
            "suggestions": [],
            "error": None
        }

        try:
            if intent == "loan_types":
                response["text"] = "We offer several types of loans:\n" + \
                    "\n".join(f"- {loan}" for loan in self.knowledge_base["loan"]["types"])
                response["suggestions"] = ["Tell me about interest rates", "How to check credit score"]

            elif intent == "credit_score_info":
                info = self.knowledge_base["credit_score"]
                response["text"] = f"Credit score is {info['definition']}.\n" + \
                    f"Score range: {info['range']}\n" + \
                    f"Key factors affecting credit score:\n" + \
                    "\n".join(f"- {factor}" for factor in info["factors"])
                response["suggestions"] = ["How to improve credit score", "Apply for loan"]

            elif intent == "interest_rates":
                info = self.knowledge_base["interest_rate"]
                response["text"] = f"Interest rate is {info['definition']}.\n" + \
                    f"Types of interest rates:\n" + \
                    "\n".join(f"- {rate_type}" for rate_type in info["types"])
                response["suggestions"] = ["Calculate EMI", "Compare loan options"]

            elif intent in self.knowledge_base:
                info = self.knowledge_base[intent]
                response["text"] = f"{intent.replace('_', ' ').title()}: {info['definition']}"
                response["suggestions"] = ["Learn more", "Talk to an advisor"]

            else:
                response["text"] = "I'm not sure about that. Would you like to know about loans, credit scores, or interest rates?"
                response["suggestions"] = ["Loan Types", "Credit Score", "Interest Rates"]

        except Exception as e:
            response["error"] = str(e)
            response["text"] = "I encountered an error processing your request. Please try again."

        return response

# Streamlit web interface
def main():
    st.set_page_config(
        page_title="FinTech Chatbot",
        page_icon="💰",
        layout="centered"
    )

    st.title("FinTech Chatbot 💰")
    st.write("Ask me about loans, credit scores, and interest rates!")

    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FintechChatbot()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get chatbot response
        response = st.session_state.chatbot.get_response(user_input)
        
        # Add bot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response["text"]})
        
        # Show suggestions
        if response["suggestions"]:
            with st.expander("Suggested questions"):
                for suggestion in response["suggestions"]:
                    st.button(suggestion, key=suggestion, on_click=lambda s=suggestion: ask_suggestion(s))

def ask_suggestion(suggestion):
    # Add suggested question to chat history and get response
    st.session_state.chat_history.append({"role": "user", "content": suggestion})
    response = st.session_state.chatbot.get_response(suggestion)
    st.session_state.chat_history.append({"role": "assistant", "content": response["text"]})

if __name__ == "__main__":
    main()
