import { cn } from "@/lib/utils";

/**
 * The `SC` mark + product label.
 *
 * The label is the product name in the active locale ("Support CRM" /
 * "دعم العملاء"); there is no separate brand wordmark.
 */
export function Lockup({ product, className }: { product: string; className?: string }) {
  return (
    <div className={cn("flex min-w-0 flex-none items-center gap-[9px]", className)}>
      <div
        aria-hidden
        className="flex h-7 w-7 flex-none items-center justify-center rounded-[7px] bg-ink text-[11px] font-bold tracking-[0.03em] text-white"
      >
        SC
      </div>
      <span className="truncate text-[14px] font-bold">{product}</span>
    </div>
  );
}
