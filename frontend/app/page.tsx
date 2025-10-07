'use client';

import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { Activity, Database, Zap, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

interface MetricData {
  timestamp: string;
  value: number;
  category: string;
}

interface SystemStatus {
  kafka: 'healthy' | 'warning' | 'error';
  spark: 'healthy' | 'warning' | 'error';
  postgres: 'healthy' | 'warning' | 'error';
  airflow: 'healthy' | 'warning' | 'error';
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<MetricData[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    kafka: 'healthy',
    spark: 'healthy',
    postgres: 'healthy',
    airflow: 'healthy',
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      fetchMetrics();
      fetchSystemStatus();
    }, 5000);

    fetchMetrics();
    fetchSystemStatus();
    setIsLoading(false);

    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/metrics');
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'status-success';
      case 'warning':
        return 'status-warning';
      case 'error':
        return 'status-error';
      default:
        return 'status-indicator bg-gray-100 text-gray-800';
    }
  };

  // Mock data for demonstration
  const mockMetrics = [
    { timestamp: '2024-01-01T00:00:00Z', value: 120, category: 'A' },
    { timestamp: '2024-01-01T01:00:00Z', value: 135, category: 'A' },
    { timestamp: '2024-01-01T02:00:00Z', value: 98, category: 'B' },
    { timestamp: '2024-01-01T03:00:00Z', value: 156, category: 'A' },
    { timestamp: '2024-01-01T04:00:00Z', value: 142, category: 'B' },
    { timestamp: '2024-01-01T05:00:00Z', value: 178, category: 'A' },
  ];

  const pieData = [
    { name: 'Category A', value: 400, color: '#3b82f6' },
    { name: 'Category B', value: 300, color: '#10b981' },
    { name: 'Category C', value: 200, color: '#f59e0b' },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* System Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="flex items-center">
            <Database className="w-8 h-8 text-blue-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Kafka</p>
              <div className="flex items-center mt-1">
                {getStatusIcon(systemStatus.kafka)}
                <span className={`ml-2 ${getStatusClass(systemStatus.kafka)}`}>
                  {systemStatus.kafka}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <Zap className="w-8 h-8 text-yellow-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Spark</p>
              <div className="flex items-center mt-1">
                {getStatusIcon(systemStatus.spark)}
                <span className={`ml-2 ${getStatusClass(systemStatus.spark)}`}>
                  {systemStatus.spark}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <Database className="w-8 h-8 text-green-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">PostgreSQL</p>
              <div className="flex items-center mt-1">
                {getStatusIcon(systemStatus.postgres)}
                <span className={`ml-2 ${getStatusClass(systemStatus.postgres)}`}>
                  {systemStatus.postgres}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <Activity className="w-8 h-8 text-purple-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Airflow</p>
              <div className="flex items-center mt-1">
                {getStatusIcon(systemStatus.airflow)}
                <span className={`ml-2 ${getStatusClass(systemStatus.airflow)}`}>
                  {systemStatus.airflow}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time Data Flow */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Real-time Data Flow</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockMetrics}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Data Distribution */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Data Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Processing Metrics */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Processing Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary-600">1,234</div>
            <div className="text-sm text-gray-600">Messages Processed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">99.9%</div>
            <div className="text-sm text-gray-600">Success Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600">2.3s</div>
            <div className="text-sm text-gray-600">Avg Processing Time</div>
          </div>
        </div>
      </div>
    </div>
  );
}
