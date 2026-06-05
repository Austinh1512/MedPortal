import { Routes, Route } from "react-router-dom"

function App() {

  return (
    <Routes>
     <Route index element={<Dashboard />} />
     <Route path="login" element={<Login />} />
     <Route path="register" element={<Register />} />
     <Route path="patients" element={<PatientExplorer />} />
     <Route path="patients/:id" element={<PatientDetail />} />
    </Routes>
  )
}

export default App
