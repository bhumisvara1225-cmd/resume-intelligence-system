import { useState, useEffect, useCallback } from 'react'
import api from './api'
import './App.css'
import Header from './components/Header'
import FilterSidebar from './components/FilterSidebar'
import CandidateCard from './components/CandidateCard'
import UploadModal from './components/UploadModal'
import ResumeViewerModal from './components/ResumeViewerModal'

function App() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  // Role analysis state
  const [activeRole, setActiveRole] = useState('');
  const [roleScores, setRoleScores] = useState({});   // { candidateId: { score, keywords } }
  const [analyzingRoles, setAnalyzingRoles] = useState(false);

  // ── Helpers ──────────────────────────────────────────────────────────────

  /** Try to find a stored suitability score for the given role */
  const getStoredRoleScore = (candidate, role) => {
    if (!candidate.ai_analysis?.suitability_scores) return null;
    try {
      let scores = candidate.ai_analysis.suitability_scores;
      if (typeof scores === 'string') scores = JSON.parse(scores);
      const roleLower = role.toLowerCase();
      for (const [key, val] of Object.entries(scores)) {
        if (
          key.toLowerCase().includes(roleLower) ||
          roleLower.includes(key.toLowerCase())
        ) {
          // Normalize: some models return 0-1, others 0-100
          const n = typeof val === 'number' ? val : parseFloat(val);
          return Math.round(n <= 1 ? n * 100 : n);
        }
      }
    } catch (_) {}
    return null;
  };

  /** Score all candidates against a role, using stored data where possible */
  const analyzeForRole = useCallback(async (role, candidateList) => {
    if (!role?.trim()) {
      setActiveRole('');
      setRoleScores({});
      return;
    }
    setActiveRole(role);
    setAnalyzingRoles(true);

    const list = candidateList || candidates;
    const accumulated = {};
    const needsAPI = [];

    for (const c of list) {
      const stored = getStoredRoleScore(c, role);
      if (stored !== null) {
        accumulated[c.candidate_id] = { score: stored, keywords: [], fromStored: true };
      } else {
        needsAPI.push(c);
      }
    }

    // Show stored results immediately
    setRoleScores({ ...accumulated });

    // Fetch remaining via API
    for (const c of needsAPI) {
      try {
        const res = await api.get(
          `/api/resumes/${c.candidate_id}/score?role=${encodeURIComponent(role)}`
        );
        accumulated[c.candidate_id] = {
          score: res.data.ats_score ?? 0,
          keywords: res.data.matching_keywords ?? [],
        };
        setRoleScores({ ...accumulated }); // progressive update
      } catch (_) {
        accumulated[c.candidate_id] = { score: 0, keywords: [] };
        setRoleScores({ ...accumulated });
      }
    }

    setAnalyzingRoles(false);
  }, [candidates]);

  // ── Data fetching ─────────────────────────────────────────────────────────

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (searchQuery) params.append('search', searchQuery);
      if (selectedSkills.length > 0) params.append('skill', selectedSkills[0]);

      const url = '/api/resumes/' + (params.toString() ? '?' + params.toString() : '');
      const response = await api.get(url);
      setCandidates(response.data);

      // Re-score if a role is already active
      if (activeRole) {
        analyzeForRole(activeRole, response.data);
      }
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const t = setTimeout(fetchCandidates, 300);
    return () => clearTimeout(t);
  }, [searchQuery, selectedSkills]);

  // ── Derived sorted list ───────────────────────────────────────────────────

  const sortedCandidates = activeRole && Object.keys(roleScores).length > 0
    ? [...candidates].sort((a, b) => {
        const sa = roleScores[a.candidate_id]?.score ?? -1;
        const sb = roleScores[b.candidate_id]?.score ?? -1;
        return sb - sa;
      })
    : candidates;

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="app-container">
      <Header
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenUpload={() => setIsUploadModalOpen(true)}
      />

      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={fetchCandidates}
      />

      <ResumeViewerModal
        isOpen={!!selectedCandidate}
        onClose={() => setSelectedCandidate(null)}
        candidate={selectedCandidate}
        roleFilter={activeRole}
      />

      <main className="main-content">
        <FilterSidebar
          selectedSkills={selectedSkills}
          setSelectedSkills={setSelectedSkills}
          activeRole={activeRole}
          onAnalyzeRole={(role) => analyzeForRole(role)}
          analyzingRoles={analyzingRoles}
        />

        <div className="content-area">
          {/* Role Analysis Banner */}
          {activeRole && (
            <div className="role-banner glass">
              <div className="role-banner-left">
                <span className="role-banner-icon">🎯</span>
                <span className="role-banner-text">
                  Analyzing candidates for <strong>{activeRole}</strong>
                </span>
                {analyzingRoles && <div className="spinner-small" />}
              </div>
              <div className="role-banner-stats">
                {Object.keys(roleScores).length} / {candidates.length} scored
              </div>
            </div>
          )}

          {loading ? (
            <div className="loading-container">
              <div className="spinner" />
            </div>
          ) : sortedCandidates.length > 0 ? (
            <div className="candidate-grid">
              {sortedCandidates.map((candidate) => (
                <CandidateCard
                  key={candidate.candidate_id}
                  candidate={candidate}
                  onClick={() => setSelectedCandidate(candidate)}
                  activeRole={activeRole}
                  roleScore={roleScores[candidate.candidate_id]?.score}
                  roleKeywords={roleScores[candidate.candidate_id]?.keywords}
                />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <h2>No candidates found</h2>
              <p>Try adjusting your search or filters to find what you're looking for.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
