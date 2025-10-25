import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { ChewieChat } from '../src/ui/ChewieChat';
import { Modal } from '../src/ui/Modal';
import { FloatingButton } from '../src/ui/FloatingButton';
import { getTranslations } from '../src/core/i18n';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  const t = getTranslations('en');

  it('FloatingButton should have no a11y violations', async () => {
    const { container } = render(
      <FloatingButton
        isOpen={false}
        onClick={() => {}}
        position="bottom-right"
        ariaLabel="Open chat"
      />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('FloatingButton should have proper ARIA attributes', () => {
    const { getByRole } = render(
      <FloatingButton
        isOpen={false}
        onClick={() => {}}
        position="bottom-right"
        ariaLabel="Open Chewie Chat"
      />
    );

    const button = getByRole('button');
    expect(button).toHaveAttribute('aria-label', 'Open Chewie Chat');
    expect(button).toHaveAttribute('aria-expanded', 'false');
  });

  it('Modal should have no a11y violations when open', async () => {
    const { container } = render(
      <Modal isOpen={true} onClose={() => {}} position="bottom-right" t={t}>
        <div>Test content</div>
      </Modal>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('Modal should have proper ARIA attributes', () => {
    const { getByRole } = render(
      <Modal isOpen={true} onClose={() => {}} position="bottom-right" t={t}>
        <div>Test content</div>
      </Modal>
    );

    const dialog = getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-labelledby', 'chewie-chat-title');
  });

  it('Modal close button should be keyboard accessible', () => {
    const mockClose = vi.fn();
    const { getByLabelText } = render(
      <Modal isOpen={true} onClose={mockClose} position="bottom-right" t={t}>
        <div>Test content</div>
      </Modal>
    );

    const closeButton = getByLabelText(t.close);
    expect(closeButton).toBeTruthy();
    expect(closeButton.tagName).toBe('BUTTON');
  });

  it('ChewieChat complete widget should have no a11y violations', async () => {
    const { container } = render(
      <ChewieChat apiUrl="http://localhost:8000" mock={true} />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
