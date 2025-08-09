'use client';

import { useQuery } from '@tanstack/react-query';
import { KpiCard } from '@/components/KpiCard';
import { LineWidget } from '@/components/LineWidget';
import { DonutWidget } from '@/components/DonutWidget';
import { Users, MessageCircle, Clock, Activity } from 'lucide-react';

export default function DashboardPage() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await fetch('/api/stats', { 
        cache: 'no-store' 
      });
      if (!response.ok) {
        throw new Error('Failed to fetch stats');
      }
      return response.json();
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">Sofia Ops Dashboard</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-muted animate-pulse rounded-lg" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">Sofia Ops Dashboard</h1>
          <div className="text-red-500">Error loading dashboard data</div>
        </div>
      </div>
    );
  }

  const kpiData = stats || {
    newLeads: 42,
    activeConversations: 156,
    responseTime: 1.44,
    errorRate: 0.02,
    uptime: 99.8,
    lastUpdate: new Date().toISOString()
  };

  const performanceData = [
    { label: 'Response Time', value: kpiData.responseTime },
    { label: 'Error Rate', value: kpiData.errorRate },
    { label: 'Uptime', value: kpiData.uptime },
  ];

  const conversationData = [
    { label: 'New Users', value: kpiData.newLeads, color: '#3b82f6' },
    { label: 'Active Users', value: kpiData.activeConversations, color: '#10b981' },
  ];

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Sofia Ops Dashboard</h1>
          <div className="text-sm text-muted-foreground">
            Last update: {new Date(kpiData.lastUpdate).toLocaleString()}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KpiCard
            title="New Leads"
            value={kpiData.newLeads}
            description="Today's new leads"
            icon={<Users className="h-8 w-8" />}
            trend={{ value: 12, isPositive: true }}
          />
          <KpiCard
            title="Active Conversations"
            value={kpiData.activeConversations}
            description="Currently active"
            icon={<MessageCircle className="h-8 w-8" />}
            trend={{ value: 5, isPositive: true }}
          />
          <KpiCard
            title="Response Time"
            value={`${kpiData.responseTime}s`}
            description="Average response time"
            icon={<Clock className="h-8 w-8" />}
            trend={{ value: 8, isPositive: false }}
          />
          <KpiCard
            title="Uptime"
            value={`${kpiData.uptime}%`}
            description="Service availability"
            icon={<Activity className="h-8 w-8" />}
            trend={{ value: 0.2, isPositive: true }}
          />
        </div>

        {/* Widgets */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <LineWidget
            title="Performance Metrics"
            data={performanceData}
          />
          <DonutWidget
            title="Conversation Distribution"
            data={conversationData}
          />
        </div>
      </div>
    </div>
  );
}
