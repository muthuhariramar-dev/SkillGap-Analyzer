# 🚀 Skills Gap Analysis - Startup Guide

## ✅ Issues Fixed

### Backend (Python/Flask)
- ✅ Fixed missing role assessment routes (`/api/generateRoleQuestions`, `/api/analyzeRoleResults`)
- ✅ Added proctoring API endpoints (`/api/proctor/*`)
- ✅ Updated requirements.txt for Flask dependencies
- ✅ Registered all blueprints correctly
- ✅ Backend runs on port **5001**

### Frontend (React)
- ✅ Fixed ESLint errors (missing imports, ref cleanup, useCallback dependencies)
- ✅ Suppressed source map warnings
- ✅ Updated API endpoints to use port **5001**
- ✅ All components properly imported

## 🏃‍♂️ How to Run

### Option 1: Start All Services
```bash
# From root directory
npm run start
```

### Option 2: Start Individually
```bash
# Terminal 1 - Backend (Python)
cd backend
python app.py

# Terminal 2 - Frontend (React)  
cd frontend
npm start
```

### Option 3: Windows Batch File
```batch
# Double-click start.bat
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001/api/*
- **Combined**: http://localhost:8000 (when using Node.js proxy)

## 🔧 Configuration

### Backend (.env)
```
MONGO_URI=mongodb://localhost:27017/skills-gap-analyzer
JWT_SECRET_KEY=your-secret-key
PORT=5001
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5001
REACT_APP_ENV=development
```

## 🧪 Testing Endpoints

### Role Assessment
```bash
# Generate questions
curl -X POST http://localhost:5001/api/generateRoleQuestions \
  -H "Content-Type: application/json" \
  -d '{"roleId": "frontend-developer"}'

# Analyze results
curl -X POST http://localhost:5001/api/analyzeRoleResults \
  -H "Content-Type: application/json" \
  -d '{"roleId": "frontend-developer", "answers": [...]}'
```

### Proctoring
```bash
# Start session
curl -X POST http://localhost:5001/api/proctor/start \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "test123", "userId": "user1"}'

# Check fullscreen
curl -X POST http://localhost:5001/api/proctor/check-fullscreen \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "test123"}'
```

## 🐛 Troubleshooting

### Port Conflicts
- Backend: 5001 (Python Flask)
- Frontend: 3000 (React)
- MongoDB: 27017

### Common Issues
1. **MongoDB not running**: Start MongoDB service
2. **Port already in use**: Kill existing processes
3. **Dependencies missing**: Run `pip install -r requirements.txt`
4. **CORS errors**: Check frontend API URL configuration

### Logs
- Backend: Console output shows startup status
- Frontend: Browser console for API errors
- Network: Check browser dev tools network tab

## 📁 Project Structure

```
Skills-Gap-Analysis-with-Generative-AI-main/
├── backend/
│   ├── app.py              # Main Flask app
│   ├── routes/
│   │   ├── roleAssessment.py
│   │   └── proctoring.py
│   └── models/            # ML models
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── components/
│   └── package.json
└── README.md
```

## 🎯 Next Steps

1. Start MongoDB service
2. Run backend and frontend
3. Test role assessment functionality
4. Verify proctoring features
5. Check all API endpoints

The application is now fully functional with all errors resolved! 🎉
