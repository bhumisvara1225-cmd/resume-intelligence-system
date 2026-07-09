import React from 'react';
import { Search, Upload } from 'lucide-react';

const Header = ({ searchQuery, setSearchQuery, onOpenUpload }) => {
  return (
    <header className="header glass">
      <div className="header-title">
        TalentIQ Resume Intelligence
      </div>
      <div className="search-container" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <div style={{ position: 'relative', width: '100%' }}>
          <Search className="search-icon" size={20} />
          <input
            type="text"
            className="search-input glass-input"
            placeholder="Search by name, email, or keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <button 
          onClick={onOpenUpload}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            background: 'var(--accent-color)',
            color: 'white',
            border: 'none',
            padding: '0.75rem 1rem',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '600',
            whiteSpace: 'nowrap'
          }}
        >
          <Upload size={18} />
          Upload Resume
        </button>
      </div>
    </header>
  );
};

export default Header;
