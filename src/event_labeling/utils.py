import sys
# sys.path.append("/home/grads/h/hasnat.md.abdullah/Snap_n_Spot/")
from transformers import pipeline
import os
# os.environ['HF_HOME'] = "/scratch/user/hasnat.md.abdullah/Snap_n_Spot/src/cachedir"
class LightweightTimeExtractor:
    def __init__(self):
        """
        Initialize with a question-answering pipeline using a smaller BERT model
        """
        self.qa_pipeline = pipeline(
            "question-answering",
            model="deepset/tinyroberta-squad2",  # Much smaller model
            device="cpu",
            cache_dir = "cachedir"
        )
    
    def extract_event(self,text:str):
       event_question ="what is the event?"
       event_answer = self.qa_pipeline(
            question=event_question,
            context=text
        )
       confidence_score_q = "What is the confidence score?"
       confidence_score_a = self.qa_pipeline(
            question=confidence_score_q,
            context=text
        )
       reasoning_q = "What is the reasoning?"
       reasoning_a = self.qa_pipeline(
            question=reasoning_q,
            context=text
        )
       extracted_data ={
            "event": event_answer['answer'],
            "confidence": confidence_score_a['answer'],
            "reasoning": reasoning_a['answer']
       }
       return extracted_data
    
   