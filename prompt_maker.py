
class Prompter:
   @staticmethod 
   def get_prompt(user_input): 
     pass 

class MuseumPrompt(Prompter):
    @staticmethod
    def get_prompt(user_input):
        prompt = f"You're a museum tour guide, answer tourist's question: {user_input}" 
        return prompt
   
