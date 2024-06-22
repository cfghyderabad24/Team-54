/**
 * Utility function to combine class names conditionally.
 * @param classes - An array of class names.
 * @returns A single string of class names separated by a space.
 */
export const cn = (...classes: (string | undefined | false | null)[]): string => {
    return classes.filter(Boolean).join(' ');
  };
  