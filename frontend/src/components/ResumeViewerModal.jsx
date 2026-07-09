import React, { useState, useEffect } from 'react';
import api from '../api';
import { X, User, Briefcase, FileText, Crosshair } from 'lucide-react';
import './ResumeViewerModal.css';

const ResumeViewerModal = ({ isOpen, onClose, candidate, roleFilter }) => {
  const [atsScore, setAtsScore] = useState(null);
  const [matchingKeywords, setMatchingKeywords] = useState([]);
  const [loadingScore, setLoadingScore] = useState(false);
  const [targetRole, setTargetRole] = useState(roleFilter || '');

  useEffect(() => {
    if (isOpen && targetRole && candidate) {
      calculateScore();
    } else if (isOpen) {
      setAtsScore(candidate?.ai_analysis?.ats_score || null);
      setMatchingKeywords([]);
    }
  }, [isOpen, candidate]);

  if (!isOpen || !candidate) return null;

  const calculateScore = async () => {
    if (!targetRole) return;
    setLoadingScore(true);
    try {
      const response = await api.get(`/api/resumes/${candidate.candidate_id}/score?role=${encodeURIComponent(targetRole)}`);
      setAtsScore(response.data.ats_score);
      setMatchingKeywords(response.data.matching_keywords || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingScore(false);
    }
  };

  const highlightText = (text, keywords) => {
    if (!text) return 'No resume text available.';
    if (!keywords || keywords.length === 0) return text;

    let highlightedText = text;
    // Sort keywords by length descending to match longer phrases first
    const sortedKeywords = [...keywords].sort((a, b) => b.length - a.length);

    sortedKeywords.forEach(keyword => {
      if (!keyword.trim()) return;
      // Use regex to replace case insensitive, avoiding replacing inside html tags if any existed (text is raw though)
      const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      highlightedText = highlightedText.replace(regex, '<mark class="highlight">$1</mark>');
    });

    return <div dangerouslySetInnerHTML={{ __html: highlightedText }} />;
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content glass resume-viewer-modal">
        <button className="close-button" onClick={onClose}>
          <X size={24} />
        </button>
        
        <div className="resume-viewer-header">
          <div className="candidate-info-row">
            <h2>{candidate.full_name}</h2>
            <div className="candidate-contact">
              {candidate.email && <span>{candidate.email}</span>}
              {candidate.phone && <span>{candidate.phone}</span>}
            </div>
          </div>
          
          <div className="ats-scoring-section glass">
            <div className="ats-scoring-inputs">
              <label><Crosshair size={16} /> Target Role:</label>
              <input 
                type="text" 
                className="glass-input role-input" 
                placeholder="e.g. Senior Frontend Developer" 
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && calculateScore()}
              />
              <button 
                className="submit-button small-button"
                onClick={calculateScore}
                disabled={loadingScore || !targetRole}
              >
                {loadingScore ? <div className="spinner-small"></div> : 'Calculate Match'}
              </button>
            </div>
            
            <div className="ats-score-display">
              <div className="score-label">Role ATS Score</div>
              <div className={`score-value ${atsScore >= 75 ? 'high' : atsScore >= 50 ? 'medium' : 'low'}`}>
                {atsScore !== null ? `${atsScore}/100` : '--'}
              </div>
            </div>
          </div>
        </div>

        <div className="resume-content-layout">
          <div className="resume-raw-text glass">
            <h3><FileText size={18} /> Resume Content</h3>
            <div className="text-scroll-area">
              {highlightText(candidate.resume_text, matchingKeywords)}
            </div>
          </div>
          
          <div className="resume-sidebar">
            <div className="sidebar-section glass">
              <h3><User size={18} /> Analysis</h3>
              <p className="summary-text">{candidate.ai_analysis?.candidate_summary}</p>
            </div>
            
            <div className="sidebar-section glass">
              <h3><Briefcase size={18} /> Extracted Skills</h3>
              <div className="skills-container">
                {candidate.skills.map((skill, idx) => (
                  <span key={idx} className={`skill-tag ${matchingKeywords.some(k => k.toLowerCase() === skill.skill_name.toLowerCase()) ? 'highlighted-tag' : ''}`}>
                    {skill.skill_name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeViewerModal;
