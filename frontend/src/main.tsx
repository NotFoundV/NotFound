import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import AnalyzePage from './pages/AnalyzePage'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AnalyzePage />
  </StrictMode>,
)
