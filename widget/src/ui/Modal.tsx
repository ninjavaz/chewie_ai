import React, { useEffect, useRef, useState } from 'react';
import type { Translations } from '../core/i18n';
import styles from './Modal.module.css';

export type ModalProps = {
  isOpen: boolean;
  onClose: () => void;
  position: 'bottom-right' | 'bottom-left';
  t: Translations;
  children: React.ReactNode;
  avatarUrl: string;
};

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  position,
  t,
  children,
  avatarUrl,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [modalPosition, setModalPosition] = useState<{ x: number; y: number } | null>(null);
  const [isResizing, setIsResizing] = useState<'top' | 'right' | 'bottom' | 'left' | 'topLeft' | 'topRight' | 'bottomLeft' | 'bottomRight' | null>(null);
  const [modalSize, setModalSize] = useState<{ width: number; height: number } | null>(null);
  const [resizeStart, setResizeStart] = useState({ x: 0, y: 0, width: 0, height: 0, left: 0, top: 0 });
  const [isMaximized, setIsMaximized] = useState(false);

  const handleMaximize = () => {
    if (isMaximized) {
      // Restore to default
      setModalSize(null);
      setModalPosition(null);
      setIsMaximized(false);
    } else {
      // Maximize
      setModalSize({ width: 400, height: window.innerHeight - 48 });
      setModalPosition(null);
      setIsMaximized(true);
    }
  };

  // Focus trap
  useEffect(() => {
    if (!isOpen) return;

    const modal = modalRef.current;
    if (!modal) return;

    const focusableElements = modal.querySelectorAll<HTMLElement>(
      'button:not(:disabled), [href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])'
    );

    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    // Focus first element
    closeButtonRef.current?.focus();

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable?.focus();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable?.focus();
        }
      }
    };

    modal.addEventListener('keydown', handleTabKey);
    return () => modal.removeEventListener('keydown', handleTabKey);
  }, [isOpen]);

  // ESC to close
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Drag functionality
  useEffect(() => {
    const header = headerRef.current;
    const modal = modalRef.current;
    if (!header || !modal) return;

    const handleMouseDown = (e: MouseEvent) => {
      // Don't drag if clicking on buttons
      if ((e.target as HTMLElement).closest('button')) return;

      setIsDragging(true);
      const rect = modal.getBoundingClientRect();
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
    };

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;

      const x = e.clientX - dragOffset.x;
      const y = e.clientY - dragOffset.y;

      // Keep modal within viewport bounds
      const maxX = window.innerWidth - modal.offsetWidth;
      const maxY = window.innerHeight - modal.offsetHeight;

      setModalPosition({
        x: Math.max(0, Math.min(x, maxX)),
        y: Math.max(0, Math.min(y, maxY)),
      });
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    header.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      header.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  // Resize functionality
  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      const deltaX = e.clientX - resizeStart.x;
      const deltaY = e.clientY - resizeStart.y;

      const newSize = { width: resizeStart.width, height: resizeStart.height };
      const newPosition = { x: resizeStart.left, y: resizeStart.top };

      // Handle horizontal resizing
      if (isResizing === 'right' || isResizing === 'topRight' || isResizing === 'bottomRight') {
        newSize.width = Math.max(400, Math.min(800, resizeStart.width + deltaX));
      } else if (isResizing === 'left' || isResizing === 'topLeft' || isResizing === 'bottomLeft') {
        const newWidth = Math.max(400, Math.min(800, resizeStart.width - deltaX));
        newSize.width = newWidth;
        newPosition.x = resizeStart.left + (resizeStart.width - newWidth);
      }

      // Handle vertical resizing
      if (isResizing === 'bottom' || isResizing === 'bottomLeft' || isResizing === 'bottomRight') {
        newSize.height = Math.max(400, Math.min(window.innerHeight - 48, resizeStart.height + deltaY));
      } else if (isResizing === 'top' || isResizing === 'topLeft' || isResizing === 'topRight') {
        const newHeight = Math.max(400, Math.min(window.innerHeight - 48, resizeStart.height - deltaY));
        newSize.height = newHeight;
        newPosition.y = resizeStart.top + (resizeStart.height - newHeight);
      }

      setModalSize(newSize);
      if (isResizing === 'left' || isResizing === 'top' || isResizing === 'topLeft' || isResizing === 'topRight' || isResizing === 'bottomLeft') {
        setModalPosition(newPosition);
      }
    };

    const handleMouseUp = () => {
      setIsResizing(null);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing, resizeStart]);

  const handleResizeStart = (direction: 'top' | 'right' | 'bottom' | 'left' | 'topLeft' | 'topRight' | 'bottomLeft' | 'bottomRight') => (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const modal = modalRef.current;
    if (!modal) return;

    const rect = modal.getBoundingClientRect();
    setIsResizing(direction);
    setResizeStart({
      x: e.clientX,
      y: e.clientY,
      width: rect.width,
      height: rect.height,
      left: rect.left,
      top: rect.top,
    });
  };

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      className={`${styles.modal} ${styles[position]}`}
      style={{
        ...(modalPosition ? {
          left: `${modalPosition.x}px`,
          top: `${modalPosition.y}px`,
          right: 'auto',
          bottom: 'auto',
        } : {}),
        ...(modalSize ? {
          width: `${modalSize.width}px`,
          height: `${modalSize.height}px`,
        } : {}),
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="chewie-chat-title"
    >
      <div ref={headerRef} className={styles.header}>
        <div className={styles.headerLeft}>
          <div className={styles.logoIcon}>
            {avatarUrl.startsWith('http') || avatarUrl.startsWith('/') ? (
              <img src={avatarUrl} alt="ChewieAI" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <span>{avatarUrl}</span>
            )}
          </div>
          <div className={styles.headerContent}>
            <h2 id="chewie-chat-title" className={styles.title}>
              ChewieAI DeFi buddy
            </h2>
            <div className={styles.status}>
              <span className={styles.statusDot}></span>
              <span className={styles.statusText}>Online</span>
            </div>
          </div>
        </div>
        <div className={styles.headerRight}>
          <button
            type="button"
            className={styles.maximizeButton}
            onClick={handleMaximize}
            aria-label={isMaximized ? "Restore" : "Maximize"}
            title={isMaximized ? "Restore to default size" : "Maximize"}
          >
            {isMaximized ? (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3" />
              </svg>
            ) : (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3" />
              </svg>
            )}
          </button>
          {/* <button
            type="button"
            className={styles.helpButton}
            aria-label="Help"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </button> */}
          <button
            ref={closeButtonRef}
            type="button"
            className={styles.closeButton}
            onClick={onClose}
            aria-label={t.close}
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>

      <div className={styles.content}>{children}</div>
      
      {/* Resize handles - edges */}
      <div 
        className={`${styles.resizeHandle} ${styles.top}`}
        onMouseDown={handleResizeStart('top')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.right}`}
        onMouseDown={handleResizeStart('right')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.bottom}`}
        onMouseDown={handleResizeStart('bottom')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.left}`}
        onMouseDown={handleResizeStart('left')}
      />
      
      {/* Resize handles - corners */}
      <div 
        className={`${styles.resizeHandle} ${styles.topLeft}`}
        onMouseDown={handleResizeStart('topLeft')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.topRight}`}
        onMouseDown={handleResizeStart('topRight')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.bottomLeft}`}
        onMouseDown={handleResizeStart('bottomLeft')}
      />
      <div 
        className={`${styles.resizeHandle} ${styles.bottomRight}`}
        onMouseDown={handleResizeStart('bottomRight')}
      />
    </div>
  );
};
