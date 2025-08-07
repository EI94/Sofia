import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface LineWidgetProps {
  title: string;
  data: Array<{ label: string; value: number }>;
  className?: string;
  children?: ReactNode;
}

export function LineWidget({ 
  title, 
  data, 
  className,
  children 
}: LineWidgetProps) {
  return (
    <div className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}>
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        
        {children ? (
          children
        ) : (
          <div className="space-y-3">
            {data.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  {item.label}
                </span>
                <span className="text-sm font-medium">
                  {item.value}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
