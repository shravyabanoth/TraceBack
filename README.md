# TraceBack

TraceBack is an AI-Powered Missing Person Identification System developed using Python, Streamlit, SQLite, and DeepFace face recognition.

## Features
- File Missing Person Reports
- Identify Missing Persons using Face Recognition
- View Matched Cases
- Track Active Cases
- Dashboard Statistics

## Technologies Used
- Python
- Streamlit
- SQLite
- DeepFace (FaceNet512)
- OpenCV
- TensorFlow

## How to Run

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the project

```bash
streamlit run Dashboard.py
```

## Project Structure

```text
TraceBack
│── Dashboard.py
│── database.py
│── requirements.txt
│── README.md
│
└── pages
    │── 1_File_A_Report.py
    │── 2_Identify_Person.py
    │── 3_matched_cases.py
    │── 4_Active_Cases.py
```