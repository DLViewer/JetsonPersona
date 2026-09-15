# JetsonPersona
Jetson Persona: Multimodal Edge AI Face Recognition &amp; Conversational Assistant

**JetsonPersona** is a multimodal Edge AI project built on the **NVIDIA Jetson Orin Nano**.

The project combines:

* Stereo camera vision
* Face detection and face recognition
* Person identity storage
* Microphone audio input
* Speech-to-text
* Local or connected Large Language Model (LLM)
* Text-to-speech
* Speaker audio output

The main objective is to create an intelligent embedded AI assistant that can visually recognise people, communicate with them by voice, and remember newly introduced people.

---

## Project Objective

JetsonPersona is designed as an Edge AI system capable of interacting naturally with people.

When a person appears in front of the camera, the system detects and analyses the person's face.

If the person is already registered in the identity database, JetsonPersona recognises the person and greets them by name.

For example:

```text
Camera detects face
        ↓
Face recognition
        ↓
Identity matched: David
        ↓
Speaker:
"Hello David, nice to see you again."
```

If the face is not recognised, JetsonPersona starts a voice interaction and asks for the person's name.

For example:

```text
Camera detects unknown face
        ↓
Speaker:
"Hello. I don't think we've met before.
What is your name?"
        ↓
Microphone
        ↓
Speech recognition
        ↓
User:
"My name is Peter."
        ↓
LLM / Name extraction
        ↓
Name = Peter
        ↓
Store:
Face embedding + Peter
        ↓
Speaker:
"Nice to meet you, Peter.
I'll remember you."
```

When Peter appears again later, the system should recognise him automatically.

---

# Main Functions

## 1. Camera Input

JetsonPersona uses one or more cameras for visual input.

The initial implementation will use a stereo camera.

Possible camera functions include:

* RGB image capture
* Stereo image capture
* Person detection
* Face detection
* Face alignment
* Face recognition
* Distance estimation
* Depth estimation
* Basic liveness detection

For normal face recognition, one camera image is sufficient.

Stereo vision can later provide additional information such as:

```text
Person detected
Name: Peter
Distance: 1.4 m
Recognition confidence: 92%
```

Stereo depth may also help distinguish a real three-dimensional face from a photograph or display.

---

## 2. Face Detection

The system first detects faces inside each camera frame.

Possible implementations include:

* InsightFace SCRFD
* RetinaFace
* OpenCV DNN
* YOLO-based face detection
* TensorRT-optimised detection models

The detected face region is then passed to the face recognition system.

---

## 3. Face Recognition

Face recognition should not depend on the LLM.

Instead, a dedicated computer vision model generates a numerical representation of each person's face.

This representation is called a:

```text
Face Embedding
```

Example:

```text
Peter

Face embedding:
[0.182, -0.532, 0.291, 0.774, ...]
```

A newly detected embedding is compared against stored embeddings in the person database.

Possible recognition technologies include:

* ArcFace
* InsightFace
* ONNX Runtime
* CUDA
* TensorRT

---

## 4. Person Identity Database

JetsonPersona maintains a local identity database.

The database associates a person's name with one or more face embeddings.

Example:

```text
Person ID: 0001
Name: Peter
Face Embedding: [...]
Created: 2026-09-08
Last Seen: 2026-09-08
```

The first implementation can use:

```text
SQLite
```

Possible future alternatives include:

* FAISS
* Vector databases
* PostgreSQL
* Milvus

Example database structure:

```text
people

id
name
created_at
last_seen
face_embedding
photo_path
```

---

## 5. Unknown Person Enrolment

If the detected face cannot be matched with sufficient confidence, JetsonPersona enters an enrolment state.

Example:

```text
Unknown face detected
        ↓
Ask:
"What is your name?"
        ↓
Listen to microphone
        ↓
Speech-to-text
        ↓
Extract name
        ↓
Store face + name
```

The person can therefore register naturally without manually entering their name using a keyboard.

---

## 6. Microphone Input

The microphone provides audio input for the system.

Possible Python and Linux audio interfaces include:

* ALSA
* PyAudio
* sounddevice

Audio input may also use Voice Activity Detection to determine when somebody starts and stops speaking.

Possible VAD technologies include:

* Silero VAD
* WebRTC VAD

---

## 7. Speech-to-Text

Speech-to-text converts microphone audio into text.

Example:

```text
Audio:
"My name is David."

        ↓

Speech-to-text:

"My name is David."
```

Potential implementations include:

* Whisper
* whisper.cpp
* Faster-Whisper
* NVIDIA Riva

For an embedded implementation, lightweight or quantised models are preferred.

---

## 8. Large Language Model

The LLM handles natural-language interpretation and conversation.

The LLM should not perform the actual face recognition.

Instead, its responsibilities may include:

* Understanding user speech
* Extracting a person's name
* Managing dialogue
* Generating natural responses
* Answering simple questions
* Maintaining conversational context
* Controlling system actions

For example:

```text
Input:

"My name is Peter."

LLM output:
{
    "intent": "introduce_person",
    "name": "Peter"
}
```

JetsonPersona can initially use a relatively small local instruct model.

Possible runtime systems include:

* llama.cpp
* Ollama-compatible backends
* TensorRT-LLM
* Jetson Containers
* NVIDIA optimised LLM frameworks

A small quantised model is preferred for Jetson Orin Nano.

```markdown
### Current Implementation

JetsonPersona currently uses `llama.cpp` as the local LLM inference runtime.

#### Upstream Project

- Project: `llama.cpp`
- Repository: https://github.com/ggml-org/llama.cpp
- Integrated as a Git submodule:
  `external/llama.cpp`

#### Tested Configuration

- Platform: NVIDIA Jetson Orin Nano
- CUDA: 12.6
- llama.cpp build: 10968
- Model: Qwen2.5-1.5B-Instruct-GGUF
- Quantization: Q4_K_M
- Context size: 2048
- GPU layers: 10

#### Current Test Flow

```text
Keyboard Input
      ↓
Python test program
      ↓
llama-server
      ↓
Qwen2.5 1.5B Instruct
      ↓
JSON response
      ↓
Terminal Output

---

## 9. Text-to-Speech

Text-to-speech converts the system response into spoken audio.

Example:

```text
Text:

"Hello Peter. Nice to see you again."

        ↓
Text-to-Speech

        ↓

Speaker
```

Possible TTS engines include:

* Piper
* NVIDIA Riva
* Other ONNX-based TTS engines

---

## 10. Speaker Output

The generated speech is played through an external speaker.

Possible audio output interfaces include:

* USB audio
* HDMI audio
* Bluetooth audio
* USB DAC
* External sound card

---

# Hardware Platform

The initial target platform is:

## NVIDIA Jetson Orin Nano

Planned hardware:

| Component               | Function                                            |
| ----------------------- | --------------------------------------------------- |
| NVIDIA Jetson Orin Nano | Main Edge AI computing platform                     |
| Stereo Camera           | Visual input and depth information                  |
| Samsung 512 GB NVMe SSD | Operating system, AI models and database            |
| Microphone              | Voice input                                         |
| Speaker                 | Voice output                                        |
| Network connection      | Development, updates and optional online LLM access |

---

# High-Level System Architecture

```text
                         ┌──────────────────────┐
                         │    Stereo Camera     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Face Detection     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Face Recognition    │
                         │  Face Embedding      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Identity Database    │
                         │ SQLite / Vectors     │
                         └──────────┬───────────┘
                                    │
                            Face recognised?
                              /           \
                           YES             NO
                            │               │
                            ▼               ▼
                     Known Person     Unknown Person
                            │               │
                            │               ▼
                            │         Ask for name
                            │               │
                            │               ▼
                            │          Microphone
                            │               │
                            │               ▼
                            │        Speech-to-Text
                            │               │
                            │               ▼
                            │              LLM
                            │               │
                            │               ▼
                            │       Extract person name
                            │               │
                            │               ▼
                            │       Store face + name
                            │               │
                            └───────┬───────┘
                                    │
                                    ▼
                              Text-to-Speech
                                    │
                                    ▼
                                  Speaker
```

---

# Software Architecture

Python will be used as the main integration and application language.

Performance-critical AI operations can still run through:

* CUDA
* TensorRT
* ONNX Runtime
* C/C++ libraries

Python therefore acts primarily as the orchestration layer connecting the different subsystems.

---

# Proposed Source Structure

```text
JetsonPersona/
│
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── config.yaml
│
├── jetson_persona/
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   ├── stereo_camera.py
│   │   ├── face_detector.py
│   │   ├── face_recognizer.py
│   │   ├── face_embedding.py
│   │   ├── depth.py
│   │   └── liveness.py
│   │
│   ├── identity/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── matcher.py
│   │   ├── enrolment.py
│   │   └── person.py
│   │
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── microphone.py
│   │   ├── speaker.py
│   │   └── vad.py
│   │
│   ├── speech/
│   │   ├── __init__.py
│   │   ├── stt.py
│   │   └── tts.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── dialogue.py
│   │   ├── intent.py
│   │   └── name_parser.py
│   │
│   ├── controller/
│   │   ├── __init__.py
│   │   ├── state_machine.py
│   │   └── interaction.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── timing.py
│
├── models/
│   ├── face/
│   ├── speech/
│   ├── llm/
│   └── tts/
│
├── data/
│   ├── database/
│   │   └── people.db
│   │
│   ├── faces/
│   ├── audio/
│   └── logs/
│
├── scripts/
│   ├── test_camera.py
│   ├── test_face_detection.py
│   ├── test_microphone.py
│   ├── test_speaker.py
│   ├── test_stt.py
│   └── test_tts.py
│
├── tests/
│
└── docs/
```

---

# Application State Machine

The application can be implemented as an event-driven state machine.

Example states:

```text
IDLE
  │
  ▼
FACE_DETECTED
  │
  ▼
IDENTIFY_PERSON
  │
  ├── Known
  │      ↓
  │    GREET_PERSON
  │
  └── Unknown
         ↓
      ASK_NAME
         ↓
      LISTENING
         ↓
      SPEECH_RECOGNITION
         ↓
      EXTRACT_NAME
         ↓
      ENROL_PERSON
         ↓
      CONFIRM_ENROLMENT
         ↓
        IDLE
```

This design avoids running every AI model continuously and helps reduce GPU, CPU and memory usage.

---

# Development Roadmap

## Phase 1 — Basic Camera and Face Detection

Target:

```text
Camera
   ↓
Face Detection
   ↓
Bounding Box
```

Tasks:

* Configure Jetson camera input
* Capture frames using OpenCV/GStreamer
* Detect faces
* Display bounding boxes
* Measure processing speed

---

## Phase 2 — Face Recognition

Target:

```text
Camera
   ↓
Face Detection
   ↓
Face Embedding
   ↓
Database Matching
   ↓
Person Name
```

Tasks:

* Add face embedding model
* Implement similarity calculation
* Create identity database
* Register known test persons
* Display recognition confidence

---

## Phase 3 — Text-to-Speech

Target:

```text
Recognised Person
        ↓
"Hello Peter"
        ↓
Speaker
```

Tasks:

* Configure speaker output
* Install TTS engine
* Generate spoken greetings

---

## Phase 4 — Microphone and Speech Recognition

Target:

```text
Microphone
    ↓
Speech Detection
    ↓
Speech-to-Text
```

Tasks:

* Configure microphone
* Add Voice Activity Detection
* Add Whisper or equivalent STT
* Convert speech into text

---

## Phase 5 — New Person Enrolment

Target:

```text
Unknown Face
     ↓
Ask Name
     ↓
Listen
     ↓
Recognise Speech
     ↓
Extract Name
     ↓
Store Face + Name
```

This phase produces the core JetsonPersona behaviour.

---

## Phase 6 — LLM Integration

Add conversational intelligence.

Potential functions:

* Name extraction
* Intent detection
* Natural greeting generation
* Follow-up questions
* Conversation context
* User interaction logic

---

## Phase 7 — Stereo Vision

Add depth information.

Potential functions:

* Distance estimation
* Person localisation
* Depth-based filtering
* Liveness assistance
* Multiple-person tracking

---

## Phase 8 — Advanced Persona Memory

Future versions may store additional non-sensitive interaction information such as:

```text
Person:
Peter

Last seen:
2026-09-08

Number of visits:
5

Preferred greeting:
Hello Peter
```

Privacy, consent, retention and deletion controls should be designed before storing additional personal information.

---

# Initial Technology Candidates

| Subsystem                | Candidate                |
| ------------------------ | ------------------------ |
| Main language            | Python                   |
| Camera                   | OpenCV / GStreamer       |
| Stereo processing        | OpenCV / Camera SDK      |
| Face detection           | InsightFace SCRFD        |
| Face recognition         | ArcFace / InsightFace    |
| AI inference             | ONNX Runtime / TensorRT  |
| Database                 | SQLite                   |
| Vector matching          | NumPy / FAISS            |
| Voice activity detection | Silero VAD               |
| Speech-to-text           | Whisper / whisper.cpp    |
| LLM                      | llama.cpp / TensorRT-LLM |
| Text-to-speech           | Piper                    |
| GPU                      | CUDA                     |
| Storage                  | NVMe SSD                 |

The exact software components may change as JetsonPersona is developed and benchmarked on the Jetson Orin Nano.

---

# Design Principles

JetsonPersona should follow several important design principles.

### Edge First

Where practical, AI processing should run locally on the Jetson device.

Benefits include:

* Reduced latency
* Better privacy
* Reduced cloud dependency
* Offline operation
* Lower network requirements

### Modular Architecture

Vision, speech, LLM and identity management should remain independent modules.

This allows individual technologies to be replaced without rewriting the whole application.

### Event-Driven Processing

High-compute models should only run when required.

For example:

```text
No person detected
→ Do not run speech recognition
→ Do not run LLM
→ Do not run TTS
```

### Explicit Identity Confidence

A person should only be considered recognised when similarity exceeds a configured threshold.

Low-confidence matches should be treated as unknown rather than incorrectly assigning an identity.

### Privacy by Design

Face embeddings and personal names are biometric/personal information.

The project should eventually support:

* User consent
* Local storage
* Database deletion
* Identity removal
* Configurable retention
* Secure storage
* Clear enrolment behaviour

---

# Example Target Scenario

### First Meeting

```text
JetsonPersona:
"Hello. I don't think we've met before.
What is your name?"

Person:
"My name is David."

JetsonPersona:
"Nice to meet you, David.
I'll remember you."
```

The system stores:

```text
David
+
Face embedding
```

### Next Meeting

The same person approaches the camera.

```text
Face detected
      ↓
Face embedding generated
      ↓
Database match
      ↓
David
```

JetsonPersona responds:

```text
"Hello David. Nice to see you again."
```

---

# Project Status

**Status: Initial Architecture / Prototype Development**

Current target:

```text
Jetson Orin Nano
+
Stereo Camera
+
NVMe SSD
+
Microphone
+
Speaker
+
Python
```

Initial development will focus on establishing reliable face detection and face recognition before adding the complete voice and LLM interaction pipeline.

---

# Long-Term Vision

The long-term target of JetsonPersona is to demonstrate how multiple AI technologies can be integrated into a single embedded Edge AI platform.

The project combines:

```text
Computer Vision
       +
Face Recognition
       +
Stereo Vision
       +
Speech Recognition
       +
Large Language Models
       +
Text-to-Speech
       +
Embedded AI
       =
JetsonPersona
```

The system may eventually evolve from a face-recognition demonstrator into a general-purpose visual and conversational Edge AI assistant.

---

## Project Name

**JetsonPersona**

**Multimodal Edge AI Face Recognition and Conversational Assistant**

Platform:

**NVIDIA Jetson Orin Nano**
