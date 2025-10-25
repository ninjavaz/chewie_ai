import React from 'react';
import type { EarningsData } from '../core/types';
import type { Translations } from '../core/i18n';
import styles from './EarningsCard.module.css';

export type EarningsCardProps = {
  earnings: EarningsData;
  t: Translations;
  amount?: number;
  currency?: string;
};

export const EarningsCard: React.FC<EarningsCardProps> = ({
  earnings,
  t,
  amount = 1000,
  currency = 'USDC',
}) => {
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatPercent = (value: number): string => {
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.icon}>💰</span>
        <span className={styles.title}>{t.earnings.title}</span>
      </div>
      
      <div className={styles.main}>
        <div className={styles.amount}>
          {amount.toLocaleString()} {currency}
        </div>
        <div className={styles.arrow}>→</div>
        <div className={styles.result}>
          <span className={styles.earnings}>+{formatCurrency(earnings.yearly)}</span>
          <span className={styles.period}>/{t.earnings.yearly}</span>
        </div>
      </div>

      <div className={styles.details}>
        <div className={styles.detail}>
          <span className={styles.label}>{t.earnings.apr}:</span>
          <span className={styles.value}>{formatPercent(earnings.apr)}</span>
        </div>
        {earnings.updatedAt && (
          <div className={styles.updated}>
            {t.earnings.updated} {earnings.updatedAt}
          </div>
        )}
      </div>
    </div>
  );
};
