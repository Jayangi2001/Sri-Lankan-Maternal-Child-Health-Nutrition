import os
import subprocess
import time
from google.colab import userdata
from google.colab import output

os.environ["GROQ_API_KEY"] = userdata.get('GROQ_API_KEY')
os.environ["OPENROUTER_API_KEY"] = userdata.get('OPENROUTER_API_KEY')

print("API Keys loaded securely from Colab Secrets!")

!pkill -f streamlit

subprocess.Popen([
    "streamlit", "run", "app.py",
    "--server.port", "8501",
    "--server.address", "0.0.0.0",
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false",
    "--server.headless", "true"
])

time.sleep(4)

url = output.eval_js("google.colab.kernel.proxyPort(8501)")
print("\n" + "="*60)
print("👉 Click this link to open your Streamlit App:")
print(url)
print("="*60 + "\n")
