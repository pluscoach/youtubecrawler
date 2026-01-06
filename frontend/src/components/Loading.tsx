export default function Loading({ message = '분석하고 있습니다...' }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="w-12 h-12 border-4 border-border border-t-accent rounded-full animate-spin mb-4" />
      <p className="text-text-secondary animate-pulse">{message}</p>
    </div>
  );
}
