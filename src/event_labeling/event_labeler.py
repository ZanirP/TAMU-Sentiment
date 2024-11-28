import sys
#sys.path.append("/src/event_labeling")
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
from typing import List, Dict, Optional
import json
from collections import defaultdict
from src.event_labeling.utils import LightweightTimeExtractor
class TweetEventLabeler:
    def __init__(
        self,
        predefined_events: List[str],
        model_name: str = "microsoft/phi-2",  # Small but capable instruction-following model
        confidence_threshold: float = 0.65,
        max_length: int = 128,
        instruction_template: str = None
    ):
        """
        Initialize the event labeler with instruction-based model.
        
        Args:
            predefined_events: List of predefined event labels
            model_name: HuggingFace model to use (default: phi-2)
            confidence_threshold: Minimum confidence score to assign a new event
            max_length: Maximum length of input text to process
            instruction_template: Custom instruction template for the model
        """
        self.predefined_events = predefined_events
        self.confidence_threshold = confidence_threshold
        self.max_length = max_length
        
        # Default instruction template
        self.instruction_template = instruction_template or """
Given a tweet, classify it into one of these predefined events: {events}
If the tweet doesn't match any predefined event with high confidence, create a new descriptive event name.
Rules for new event names:
1. Use lowercase with underscores
2. Be concise (2-4 words)
3. Be descriptive of the main event
4. If no clear event can be identified, return "unk_event"

Tweet: {tweet}

Think step by step:
1. What is the main topic/event in this tweet?
2. Does it match any predefined events? If yes, which one?
3. If no match, what would be a good new event name?

Respond in JSON format:
{{"event": "event_name", "confidence": confidence_score, "reasoning": "brief explanation"}}
"""
        
        # Directory to save the model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "microsoft/phi-2"

        # Load the model and tokenizer from the saved directory
        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                                          trust_remote_code=True,
                                                          torch_dtype=torch.float16,
                                                          trust_remote_code=True
                                                        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def clean_tweet(self, tweet: str) -> str:
        """Clean tweet text by removing URLs, mentions, and special characters."""
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        tweet = ' '.join(tweet.split())
        return tweet

    def get_model_response(self, prompt: str) -> str:
        """Get response from the instruction-following model."""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, 
                              max_length=self.max_length).to(self.device)
        
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=256,
            temperature=0.5,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Model response: {response}")
        return response.strip()


    def extract_json_from_response(self, response: str, llm_labeler=None) -> Dict:
        """
        Extract JSON from model response.
        Args:
            response: String containing a JSON object somewhere in the text
        Returns:
            Dictionary containing the parsed JSON or an error object
        """

        try:
            pattern = r'{"event":\s*"(.*?)",\s*"confidence":\s*(\d+\.\d+),\s*"reasoning":\s*"(.*?)"}'
    
            # Search for the expected part in the tweet analysis output
            match = re.search(pattern, response)
            
            if match:
                # Extract event, confidence, and reasoning
                event = match.group(1)
                confidence = float(match.group(2))
                reasoning = match.group(3)
                extracted_data = {
                    "event": event,
                    "confidence": confidence,
                    "reasoning": reasoning
                }
                return extracted_data
            else:  
                extracted_data = llm_labeler.extract_event(response)
            if extracted_data:
                return extracted_data
        
            return {"event": "unk_event", "confidence": 0.0, "reasoning": "Failed to parse response"}

            
        except json.JSONDecodeError as je:
            print(f"JSON parsing error: {je}")
            return {
                "event": "unk_event",
                "confidence": 0.0,
                "reasoning": f"JSON Parse Error: {str(je)}"
            }
        except Exception as e:
            print(f"General error: {e}")
            return {
                "event": "unk_event",
                "confidence": 0.0,
                "reasoning": f"Error: {str(e)}"
            }
    # def extract_json_from_response(self, response: str) -> Dict:
    #     """Extract JSON from model response."""
    #     try:
    #         # Find JSON-like structure in the response
    #         match = re.search(r'\{.*\}', response, re.DOTALL)
    #         if match:
    #             json_str = match.group()
    #             result = json.loads(json_str)
    #             return result
    #         return {"event": "unk_event", "confidence": 0.0, "reasoning": "Failed to parse response"}
    #     except Exception as e:
    #         print(f"Error parsing response: {e}")
    #         return {"event": "unk_event", "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

    def label_event(self, tweet: str, custom_instruction: str = None, llm_labeler=None) -> Dict:
        """
        Label a tweet using the instruction-based model.
        
        Args:
            tweet: The tweet to label
            custom_instruction: Optional custom instruction for this specific tweet
            
        Returns:
            Dict containing event label, confidence score, and reasoning
        """
        # cleaned_tweet = self.clean_tweet(tweet)
        
        # if not cleaned_tweet:
        #     return {"event": "unk_event", "confidence": 0.0, "reasoning": "Empty tweet after cleaning"}
        
        # Format instruction
        instruction = custom_instruction or self.instruction_template
        prompt = instruction.format(
            events=", ".join(self.predefined_events),
            tweet=tweet
        )
        
        # Get model response
        response = self.get_model_response(prompt)
        result = self.extract_json_from_response(response,llm_labeler=llm_labeler)
        

        # Ensure required fields exist
        # result.setdefault("event", "unk_event")
        # result.setdefault("confidence", 0.0)
        # result.setdefault("reasoning", "No reasoning provided")
        
        return result

def main():

    llm_labeler = LightweightTimeExtractor()
    # Example usage
    predefined_events = [

    ]
    
    # Custom instruction example
    custom_instruction = """
Analyze theses tweet and categorize it into one of these events: {events}
If none match, create a new event category that is specific but not too narrow.
Focus on the main action or happening, not minor details.

Tweets: {tweet}

Provide your analysis as JSON:
{{"event": "event_name", "confidence": 0.0-1.0, "reasoning": "why you chose this category"}}
"""
    
    # Initialize the labeler
    labeler = TweetEventLabeler(
        predefined_events=predefined_events,
        instruction_template=custom_instruction
    )
    
    # # Example tweets
    # sample_tweets = [
    #     "Breaking: Magnitude 7.2 earthquake hits coastal region, tsunami warning issued",
    #     "New smartphone launch event scheduled for next week with revolutionary features",
    #     "Local community organizes beach cleanup drive, hundreds participate",
    # ]
    cluster_json_path = "src/event_labeling/devan_packaged_clusters.json"
    # cluster_json_path = "/scratch/user/hasnat.md.abdullah/TAMU-Sentiment/src/event_labeling/packaged_clusters.json"
    with open(cluster_json_path, "r") as f:
        clusters = json.load(f)
    
    for cluster in clusters: 
        cluster_id = cluster['cluster_id']
        documents:list = cluster['documents']
        
        tracker = defaultdict(int)
        for tweet in documents:
            result = labeler.label_event(tweet["Text"], llm_labeler=llm_labeler)
            tracker[result['event']] += 1
            print(f"tracker: {tracker}")
            # break

        print(f"Cluster ID: {cluster_id}")
        print(f"tracker: {tracker}")
        most_common_event = max(tracker, key=tracker.get)
        print(f"Most common event: {most_common_event} with count: {tracker[most_common_event]}")
        # print(f"result: {result}")
        # print(f"\nTweet: {documents}")
        # print(f"Event: {result['event']}")
        # print(f"Confidence: {result['confidence']:.2f}")
        # print(f"Reasoning: {result['reasoning']}")
        # print("-" * 40)
        # break
    # Process tweets
    # for tweet in sample_tweets:
    #     result = labeler.label_event(tweet)
    #     print(f"result: {result}")
    #     print(f"\nTweet: {tweet}")
    #     print(f"Event: {result['event']}")
    #     print(f"Confidence: {result['confidence']:.2f}")
    #     print(f"Reasoning: {result['reasoning']}")
    #     print("-" * 40)
        # break

if __name__ == "__main__":
    main()
