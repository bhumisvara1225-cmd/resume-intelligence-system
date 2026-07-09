import React, { useState } from 'react';
import { Target, Zap, X } from 'lucide-react';

const COMMON_SKILLS = [
  'Python', 'React', 'JavaScript', 'SQL', 'AWS',
  'Docker', 'Machine Learning', 'FastAPI', 'Node.js', 'TypeScript',
];

const QUICK_ROLES = [
  // Engineering
  'Full Stack Developer',
  'Frontend Developer',
  'Backend Developer',
  'Software Engineer',
  'Mobile Developer',
  'iOS Developer',
  'Android Developer',
  'React Developer',
  'Node.js Developer',
  'Python Developer',
  'Java Developer',
  'Golang Developer',

  // Data & AI
  'Data Scientist',
  'Data Analyst',
  'Data Engineer',
  'ML Engineer',
  'AI Engineer',
  'NLP Engineer',
  'Computer Vision Engineer',
  'Business Intelligence Analyst',

  // Cloud & Infrastructure
  'DevOps Engineer',
  'Cloud Engineer',
  'AWS Solutions Architect',
  'Site Reliability Engineer',
  'Platform Engineer',
  'Kubernetes Engineer',

  // Design & Product
  'UI/UX Designer',
  'Product Manager',
  'Product Designer',
  'Technical Writer',

  // Security & QA
  'Cybersecurity Analyst',
  'QA Engineer',
  'Penetration Tester',

  // Management
  'Engineering Manager',
  'Tech Lead',
  'Scrum Master',
];

const FilterSidebar = ({
  selectedSkills,
  setSelectedSkills,
  activeRole,
  onAnalyzeRole,
  analyzingRoles,
}) => {
  const [customRole, setCustomRole] = useState('');

  const toggleSkill = (skill) => {
    setSelectedSkills(
      selectedSkills.includes(skill)
        ? selectedSkills.filter((s) => s !== skill)
        : [...selectedSkills, skill]
    );
  };

  const handleAnalyze = (role) => {
    onAnalyzeRole(role || customRole);
  };

  const handleClear = () => {
    setCustomRole('');
    onAnalyzeRole('');
  };

  return (
    <aside className="sidebar glass">

      {/* ── Role Analysis ─────────────────────────────────── */}
      <div className="filter-section">
        <h3><Target size={13} style={{ display: 'inline', marginRight: 6 }} />Role Analysis</h3>

        <div className="role-input-row">
          <input
            type="text"
            className="glass-input role-analyze-input"
            placeholder="e.g. Full Stack Developer"
            value={customRole}
            onChange={(e) => setCustomRole(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
          />
          <button
            className={`analyze-btn ${analyzingRoles ? 'analyzing' : ''}`}
            onClick={() => handleAnalyze()}
            disabled={!customRole.trim() || analyzingRoles}
            title="Analyze all candidates for this role"
          >
            {analyzingRoles ? <div className="spinner-tiny" /> : <Zap size={14} />}
          </button>
        </div>

        {activeRole && (
          <div className="active-role-pill">
            <span>🎯 {activeRole}</span>
            <button className="clear-role-btn" onClick={handleClear} title="Clear role filter">
              <X size={12} />
            </button>
          </div>
        )}

        <div className="quick-roles-grid">
          {QUICK_ROLES.map((role) => (
            <button
              key={role}
              className={`quick-role-chip ${activeRole === role ? 'chip-active' : ''}`}
              onClick={() => {
                setCustomRole(role);
                handleAnalyze(role);
              }}
            >
              {role}
            </button>
          ))}
        </div>
      </div>

      {/* ── Skills Filter ─────────────────────────────────── */}
      <div className="filter-section">
        <h3>Top Skills</h3>
        <div className="filter-group">
          {COMMON_SKILLS.map((skill) => (
            <label key={skill} className="filter-label">
              <input
                type="checkbox"
                className="filter-checkbox"
                checked={selectedSkills.includes(skill)}
                onChange={() => toggleSkill(skill)}
              />
              {skill}
            </label>
          ))}
        </div>
      </div>

    </aside>
  );
};

export default FilterSidebar;
