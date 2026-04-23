import React, {useEffect, useMemo, useRef, useState} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import {useLocation} from '@docusaurus/router';
import styles from './styles.module.css';

function isActivePath(pathname, activeBasePath, sections = []) {
  if (activeBasePath && pathname.startsWith(activeBasePath)) {
    return true;
  }

  return sections.some((section) =>
    (section.items || []).some((item) => {
      if (!item.to) {
        return false;
      }
      return pathname === item.to || pathname.startsWith(`${item.to}/`);
    }),
  );
}

function MegaMenuDesktop({
  label,
  className,
  description,
  sections = [],
  cta,
  activeBasePath,
}) {
  const {pathname} = useLocation();
  const [open, setOpen] = useState(false);
  const rootRef = useRef(null);
  const closeTimeoutRef = useRef(null);
  const panelId = useMemo(
    () => `mega-menu-${label.toLowerCase().replace(/\s+/g, '-')}`,
    [label],
  );
  const isActive = isActivePath(pathname, activeBasePath, sections);

  useEffect(() => {
    function handlePointerOrFocus(event) {
      if (!rootRef.current || rootRef.current.contains(event.target)) {
        return;
      }
      setOpen(false);
    }

    document.addEventListener('mousedown', handlePointerOrFocus);
    document.addEventListener('touchstart', handlePointerOrFocus);
    document.addEventListener('focusin', handlePointerOrFocus);

    return () => {
      if (closeTimeoutRef.current) {
        clearTimeout(closeTimeoutRef.current);
      }
      document.removeEventListener('mousedown', handlePointerOrFocus);
      document.removeEventListener('touchstart', handlePointerOrFocus);
      document.removeEventListener('focusin', handlePointerOrFocus);
    };
  }, []);

  function openMenu() {
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
    setOpen(true);
  }

  function closeMenuWithDelay() {
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
    }
    closeTimeoutRef.current = setTimeout(() => {
      setOpen(false);
      closeTimeoutRef.current = null;
    }, 140);
  }

  return (
    <div
      ref={rootRef}
      className={clsx('navbar__item', styles.megaMenuItem, open && styles.megaMenuItemOpen)}
      onMouseEnter={openMenu}
      onMouseLeave={closeMenuWithDelay}>
      <button
        type="button"
        className={clsx(
          'navbar__link',
          styles.megaMenuTrigger,
          isActive && 'navbar__link--active',
          className,
        )}
        aria-haspopup="true"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((value) => !value)}
        onFocus={openMenu}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            setOpen((value) => !value);
          }
          if (event.key === 'Escape') {
            setOpen(false);
          }
        }}>
        <span>{label}</span>
        <span className={styles.megaMenuCaret} aria-hidden="true">
          ▾
        </span>
      </button>

      <div
        id={panelId}
        className={clsx(styles.megaMenuPanel, open && styles.megaMenuPanelOpen)}
        role="group"
        onMouseEnter={openMenu}
        onMouseLeave={closeMenuWithDelay}>
        <div className={styles.megaMenuIntro}>
          <div className={styles.megaMenuEyebrow}>Explore</div>
          <div className={styles.megaMenuTitle}>{label}</div>
          {description ? (
            <p className={styles.megaMenuDescription}>{description}</p>
          ) : null}
          {cta?.to ? (
            <Link className={styles.megaMenuCta} to={cta.to}>
              {cta.label}
            </Link>
          ) : null}
        </div>

        <div className={styles.megaMenuSections}>
          {sections.map((section) => (
            <div className={styles.megaMenuSection} key={section.title}>
              <div className={styles.megaMenuSectionTitle}>{section.title}</div>
              <ul className={styles.megaMenuList}>
                {(section.items || []).map((item) => (
                  <li key={item.label}>
                    <Link
                      className={styles.megaMenuLink}
                      to={item.to}
                      onClick={() => setOpen(false)}>
                      <span className={styles.megaMenuLinkLabel}>{item.label}</span>
                      {item.description ? (
                        <span className={styles.megaMenuLinkDescription}>
                          {item.description}
                        </span>
                      ) : null}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function MegaMenuMobile({
  label,
  sections = [],
  description,
  cta,
  activeBasePath,
  onClick,
}) {
  const {pathname} = useLocation();
  const isActive = isActivePath(pathname, activeBasePath, sections);
  const [open, setOpen] = useState(isActive);

  useEffect(() => {
    if (isActive) {
      setOpen(true);
    }
  }, [isActive]);

  return (
    <li
      className={clsx('menu__list-item', {
        'menu__list-item--collapsed': !open,
      })}>
      <button
        type="button"
        className={clsx(
          'menu__link',
          'menu__link--sublist',
          'menu__link--sublist-caret',
          styles.megaMenuMobileTrigger,
          isActive && 'menu__link--active',
        )}
        onClick={() => setOpen((value) => !value)}>
        {label}
      </button>
      {open ? (
        <div className={styles.megaMenuMobilePanel}>
          {description ? (
            <p className={styles.megaMenuMobileDescription}>{description}</p>
          ) : null}
          {cta?.to ? (
            <Link className={styles.megaMenuMobileCta} to={cta.to} onClick={onClick}>
              {cta.label}
            </Link>
          ) : null}
          {sections.map((section) => (
            <div className={styles.megaMenuMobileSection} key={section.title}>
              <div className={styles.megaMenuMobileSectionTitle}>{section.title}</div>
              <ul className="menu__list">
                {(section.items || []).map((item) => (
                  <li className="menu__list-item" key={item.label}>
                    <Link className="menu__link" to={item.to} onClick={onClick}>
                      {item.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ) : null}
    </li>
  );
}

export default function MegaMenuNavbarItem({mobile = false, ...props}) {
  if (mobile) {
    return <MegaMenuMobile {...props} />;
  }
  return <MegaMenuDesktop {...props} />;
}
