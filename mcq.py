import verifiers as vf
from verifiers.utils.data_utils import extract_boxed_answer
from datasets import Dataset
import os
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")


dataset = [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "options": {
        "A": "London",
        "B": "Berlin",
        "C": "Paris",
        "D": "Madrid"
      },
      "correctAnswer": "C",
      "explanation": "Paris is the capital and largest city of France."
    },
    {
      "id": 2,
      "question": "Which planet is known as the Red Planet?",
      "options": {
        "A": "Venus",
        "B": "Mars",
        "C": "Jupiter",
        "D": "Saturn"
      },
      "correctAnswer": "B",
      "explanation": "Mars is called the Red Planet due to iron oxide (rust) on its surface."
    },
    {
      "id": 3,
      "question": "What is the largest ocean on Earth?",
      "options": {
        "A": "Atlantic Ocean",
        "B": "Indian Ocean",
        "C": "Arctic Ocean",
        "D": "Pacific Ocean"
      },
      "correctAnswer": "D",
      "explanation": "The Pacific Ocean covers approximately 63 million square miles."
    },
    {
      "id": 4,
      "question": "Who wrote 'Romeo and Juliet'?",
      "options": {
        "A": "Charles Dickens",
        "B": "William Shakespeare",
        "C": "Jane Austen",
        "D": "Mark Twain"
      },
      "correctAnswer": "B",
      "explanation": "William Shakespeare wrote this famous tragedy in the 1590s."
    },
    {
      "id": 5,
      "question": "What is the chemical symbol for gold?",
      "options": {
        "A": "Go",
        "B": "Gd",
        "C": "Au",
        "D": "Ag"
      },
      "correctAnswer": "C",
      "explanation": "Au comes from the Latin word 'aurum' meaning gold."
    },
    {
      "id": 6,
      "question": "What is the smallest prime number?",
      "options": {
        "A": "0",
        "B": "1",
        "C": "2",
        "D": "3"
      },
      "correctAnswer": "C",
      "explanation": "2 is the smallest and only even prime number."
    },
    {
      "id": 7,
      "question": "Which gas makes up approximately 78% of Earth's atmosphere?",
      "options": {
        "A": "Oxygen",
        "B": "Carbon Dioxide",
        "C": "Nitrogen",
        "D": "Argon"
      },
      "correctAnswer": "C",
      "explanation": "Nitrogen makes up about 78% of Earth's atmosphere by volume."
    },
    {
      "id": 8,
      "question": "What is the hardest natural substance on Earth?",
      "options": {
        "A": "Gold",
        "B": "Iron",
        "C": "Diamond",
        "D": "Quartz"
      },
      "correctAnswer": "C",
      "explanation": "Diamond is the hardest natural substance, rating 10 on the Mohs scale."
    },
    {
      "id": 9,
      "question": "Which continent is the largest by land area?",
      "options": {
        "A": "Africa",
        "B": "Asia",
        "C": "North America",
        "D": "Europe"
      },
      "correctAnswer": "B",
      "explanation": "Asia is the largest continent, covering about 30% of Earth's land area."
    },
    {
      "id": 10,
      "question": "What is the speed of light in a vacuum?",
      "options": {
        "A": "300,000 km/s",
        "B": "299,792,458 m/s",
        "C": "186,000 miles/s",
        "D": "All of the above"
      },
      "correctAnswer": "D",
      "explanation": "All options represent the same speed of light, just in different units."
    },
    {
      "id": 11,
      "question": "Who painted the Mona Lisa?",
      "options": {
        "A": "Vincent van Gogh",
        "B": "Pablo Picasso",
        "C": "Leonardo da Vinci",
        "D": "Michelangelo"
      },
      "correctAnswer": "C",
      "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503 and 1519."
    },
    {
      "id": 12,
      "question": "What is the largest mammal in the world?",
      "options": {
        "A": "African Elephant",
        "B": "Blue Whale",
        "C": "Giraffe",
        "D": "Hippopotamus"
      },
      "correctAnswer": "B",
      "explanation": "The Blue Whale is the largest mammal and largest animal ever known to exist."
    },
    {
      "id": 13,
      "question": "Which element has the atomic number 1?",
      "options": {
        "A": "Helium",
        "B": "Hydrogen",
        "C": "Lithium",
        "D": "Carbon"
      },
      "correctAnswer": "B",
      "explanation": "Hydrogen has atomic number 1, meaning it has one proton in its nucleus."
    },
    {
      "id": 14,
      "question": "What is the capital of Australia?",
      "options": {
        "A": "Sydney",
        "B": "Melbourne",
        "C": "Canberra",
        "D": "Perth"
      },
      "correctAnswer": "C",
      "explanation": "Canberra is the capital city of Australia, not Sydney or Melbourne."
    },
    {
      "id": 15,
      "question": "How many sides does a hexagon have?",
      "options": {
        "A": "5",
        "B": "6",
        "C": "7",
        "D": "8"
      },
      "correctAnswer": "B",
      "explanation": "A hexagon is a polygon with six sides and six angles."
    },
    {
      "id": 16,
      "question": "Which organ in the human body produces insulin?",
      "options": {
        "A": "Liver",
        "B": "Kidney",
        "C": "Pancreas",
        "D": "Heart"
      },
      "correctAnswer": "C",
      "explanation": "The pancreas produces insulin, which regulates blood sugar levels."
    },
    {
      "id": 17,
      "question": "What is the longest river in the world?",
      "options": {
        "A": "Amazon River",
        "B": "Nile River",
        "C": "Mississippi River",
        "D": "Yangtze River"
      },
      "correctAnswer": "B",
      "explanation": "The Nile River is generally considered the longest river at about 6,650 km."
    },
    {
      "id": 18,
      "question": "Which programming language was created by Guido van Rossum?",
      "options": {
        "A": "Java",
        "B": "Python",
        "C": "C++",
        "D": "JavaScript"
      },
      "correctAnswer": "B",
      "explanation": "Python was created by Guido van Rossum and first released in 1991."
    },
    {
      "id": 19,
      "question": "What is the freezing point of water in Celsius?",
      "options": {
        "A": "32°C",
        "B": "100°C",
        "C": "0°C",
        "D": "-273°C"
      },
      "correctAnswer": "C",
      "explanation": "Water freezes at 0°C (32°F) under standard atmospheric pressure."
    },
    {
      "id": 20,
      "question": "Which country has the most time zones?",
      "options": {
        "A": "United States",
        "B": "Russia",
        "C": "China",
        "D": "France"
      },
      "correctAnswer": "D",
      "explanation": "France has 12 time zones due to its overseas territories, more than any other country."
    },
    {
      "id": 21,
      "question": "What is the square root of 144?",
      "options": {
        "A": "11",
        "B": "12",
        "C": "13",
        "D": "14"
      },
      "correctAnswer": "B",
      "explanation": "The square root of 144 is 12, since 12 × 12 = 144."
    },
    {
      "id": 22,
      "question": "Which vitamin is produced when skin is exposed to sunlight?",
      "options": {
        "A": "Vitamin A",
        "B": "Vitamin B",
        "C": "Vitamin C",
        "D": "Vitamin D"
      },
      "correctAnswer": "D",
      "explanation": "Vitamin D is synthesized in the skin when exposed to UVB radiation from sunlight."
    },
    {
      "id": 23,
      "question": "What is the currency of Japan?",
      "options": {
        "A": "Yuan",
        "B": "Won",
        "C": "Yen",
        "D": "Rupee"
      },
      "correctAnswer": "C",
      "explanation": "The Japanese Yen is the official currency of Japan."
    },
    {
      "id": 24,
      "question": "Which scientist developed the theory of relativity?",
      "options": {
        "A": "Isaac Newton",
        "B": "Albert Einstein",
        "C": "Galileo Galilei",
        "D": "Stephen Hawking"
      },
      "correctAnswer": "B",
      "explanation": "Albert Einstein developed both special and general theories of relativity."
    },
    {
      "id": 25,
      "question": "How many bones are in an adult human body?",
      "options": {
        "A": "196",
        "B": "206",
        "C": "216",
        "D": "226"
      },
      "correctAnswer": "B",
      "explanation": "An adult human body typically has 206 bones."
    }
  ]

def build_dataset() -> Dataset:
    data = []
    # convert the dataset (5 sample questions to the format)
    for item in dataset:
        formatted_question = f"{item['question']}\n\n"
        for key, value in item['options'].items():
            formatted_question += f"{key}. {value}\n"
        
        data.append({
            "question": formatted_question,
            "answer": item["correctAnswer"],
            "explanation": item["explanation"]
        })
    return Dataset.from_list(data)

def evaluate_answer(completion: str, answer: str, parser: vf.XMLParser) -> float:
    response = parser.parse_answer(completion)
    return 1.0 if response.strip() == answer.strip() else 0.0

system_prompt = """
    You are a helpful assistant that answers multiple choice questions.

    You will be given a question and options. Respond with the correct option letter only out of 4 Letters, in XML format:

    <answer>option</answer>
    """

def load_environment(**kwargs) -> vf.Environment:
    dataset = build_dataset()
    parser = vf.XMLParser(["answer"], answer_field="answer")

    rubric = vf.Rubric(
    funcs=[evaluate_answer],
    weights=[1.0],
    parser=parser
    )
    
    return vf.SingleTurnEnv(
        dataset=dataset,
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric
    )
