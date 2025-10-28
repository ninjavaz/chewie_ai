/**
 * Utility function to conditionally join classNames together
 * Filters out falsy values and joins remaining classes with spaces
 * 
 * @example
 * cn('base-class', isActive && 'active', 'another-class')
 * // Returns: 'base-class active another-class' (if isActive is true)
 */
export function cn(...classes: (string | boolean | undefined)[]): string {
  return classes.filter(Boolean).join(' ');
}