/**
 * Maps summary metrics from Sofia API to dashboard format
 */

export interface SummaryMetrics {
  leadsRate: number;
  bookingsRate: number;
  p95: Array<{ t: number; v: number }>;
  successRatio: Array<{ label: string; value: number }>;
}

export interface DashboardStats {
  newLeads: number;
  activeConversations: number;
  responseTime: number;
  errorRate: number;
  uptime: number;
  lastUpdate: string;
  mockData?: boolean;
}

export function mapSummaryToDashboard(summary: SummaryMetrics): DashboardStats {
  return {
    newLeads: summary.leadsRate * 10, // Convert rate to total
    activeConversations: summary.bookingsRate * 15, // Convert rate to total
    responseTime: summary.p95[summary.p95.length - 1]?.v || 1.44, // Use latest P95 value
    errorRate: (100 - summary.successRatio[0]?.value) / 100 || 0.02, // Convert success to error rate
    uptime: 99.8,
    lastUpdate: new Date().toISOString(),
    mockData: false
  };
}

export function mapMockToDashboard(mockData: SummaryMetrics): DashboardStats {
  return {
    ...mapSummaryToDashboard(mockData),
    mockData: true
  };
}
