## Plan my weekend

This is a short script that is fun to use on a Saturday or Sunday morning. Given sailing as an option, it finds suggestions based on the wind forecast and train availability. 
The LLM (OpenAI gpt-3.5-turbo) is prompted to orchestrate a plan given the information received from the API calls. 

Data is pulled from multiple APIs including: 
- [Train station departure boards](https://lite.realtime.nationalrail.co.uk)
- [Sunrise and sunset](api.sunrisesunset.io)
- [Wind forecast](https://api.open-meteo.com)

To install the requirements run `pip install -r requirements.txt` 

To run `python main.py` 

I tested multi-agent architechture by adding a translator agent after all the tools have been called. 

<img width="412" alt="Screenshot 2024-10-22 at 21 04 13" src="https://github.com/user-attachments/assets/01f2daa1-0580-40d8-8593-d50c93c5ff57">

Some work to do involves: 
- Adding more system prompts and boundaries
- Work on the output format (potentially automate an email that gets sent on Friday evening)
