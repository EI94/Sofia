import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface DonutWidgetProps {
  title: string;
  data: Array<{ label: string; value: number; color?: string }>;
  className?: string;
  children?: ReactNode;
}

export function DonutWidget({ 
  title, 
  data, 
  className,
  children 
}: DonutWidgetProps) {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  
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
            {data.map((item, index) => {
              const percentage = total > 0 ? (item.value / total) * 100 : 0;
              return (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color || '#3b82f6' }}
                    />
                    <span className="text-sm text-muted-foreground">
                      {item.label}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium">
                      {item.value}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      ({percentage.toFixed(1)}%)
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
