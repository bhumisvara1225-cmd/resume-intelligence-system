import React from 'react';

const scoreColor = (s) =>
  s >= 75 ? '#34d399' : s >= 50 ? '#fbbf24' : '#f87171';

const CandidateCard = ({ candidate, onClick, activeRole, roleScore, roleKeywords }) => {
  // Parse suitability scores for best overall role display
  let topRoleLabel = '';
  let topRoleScore = null;
  if (candidate.ai_analysis?.suitability_scores) {
    try {
      let scores = candidate.ai_analysis.suitability_scores;
      if (typeof scores === 'string') scores = JSON.parse(scores);
      if (typeof scores === 'object' && scores !== null) {
        let best = null;
        let bestKey = '';
        for (const [key, val] of Object.entries(scores)) {
          const n = typeof val === 'number' ? val : parseFloat(val);
          const norm = n <= 1 ? n * 100 : n;
          if (best === null || norm > best) { best = norm; bestKey = key; }
        }
        if (best !== null) { topRoleLabel = bestKey; topRoleScore = Math.round(best); }
      }
    } catch (_) {}
  }

  const recentRole =
    candidate.experience?.length > 0
      ? candidate.experience[0].role
      : 'Candidate';

  const atsScore = candidate.ai_analysis?.ats_score;

  // Role-specific score display
  const showRoleScore = activeRole && roleScore !== undefined;
  const roleScoreColor = showRoleScore ? scoreColor(roleScore) : '';

  return (
    <div className="candidate-card glass" onClick={onClick}>

      {/* ── Header row ─────────────────────────────────────── */}
      <div className="candidate-header">
        <div>
          <h2 className="candidate-name">{candidate.full_name}</h2>
          <p className="candidate-title">{recentRole}</p>
        </div>

        {showRoleScore ? (
          <div
            className="score-badge role-score-badge"
            style={{
              background: `${roleScoreColor}22`,
              color: roleScoreColor,
              border: `1px solid ${roleScoreColor}55`,
            }}
          >
            {roleScore}% Match
          </div>
        ) : (
          atsScore != null && (
            <div className="score-badge">{atsScore} ATS</div>
          )
        )}
      </div>

      {/* ── Role match bar (only when role is active) ───────── */}
      {showRoleScore && (
        <div className="role-match-section">
          <div className="role-match-header">
            <span className="role-match-label">
              🎯 <strong>{activeRole}</strong>
            </span>
            <span className="role-match-pct" style={{ color: roleScoreColor }}>
              {roleScore}%
            </span>
          </div>
          <div className="role-match-track">
            <div
              className="role-match-fill"
              style={{
                width: `${roleScore}%`,
                background: `linear-gradient(90deg, ${roleScoreColor}88, ${roleScoreColor})`,
              }}
            />
          </div>
        </div>
      )}

      {/* ── Summary ─────────────────────────────────────────── */}
      <p className="candidate-summary">
        {candidate.ai_analysis?.candidate_summary ||
          'No summary available for this candidate.'}
      </p>

      {/* ── Skills ──────────────────────────────────────────── */}
      <div className="skills-container">
        {candidate.skills?.slice(0, 6).map((skill, i) => {
          const isMatch =
            roleKeywords?.some(
              (k) => k.toLowerCase() === skill.skill_name.toLowerCase()
            );
          return (
            <span
              key={i}
              className={`skill-tag ${isMatch ? 'skill-tag-match' : ''}`}
            >
              {isMatch && <span className="skill-match-dot" />}
              {skill.skill_name}
            </span>
          );
        })}
        {candidate.skills?.length > 6 && (
          <span className="skill-tag">+{candidate.skills.length - 6} more</span>
        )}
      </div>

      {/* ── Best fit role (when no active role analysis) ─────── */}
      {!showRoleScore && topRoleLabel && (
        <div className="best-fit-row">
          <span className="best-fit-label">Best fit:</span>
          <span className="best-fit-role">{topRoleLabel}</span>
          <span className="best-fit-score">{topRoleScore}%</span>
        </div>
      )}
    </div>
  );
};

export default CandidateCard;
