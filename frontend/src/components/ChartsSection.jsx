import React from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { useLanguage } from '../hooks/useLanguage';

export default function ChartsSection({ summary }) {
  const { t } = useLanguage();
  // Pie chart data for expense categories
  const expenseData = [
    { name: 'Fixed Costs', value: (summary?.monthly_expense || 0) * 0.4 },
    { name: 'Variable Costs', value: (summary?.monthly_expense || 0) * 0.35 },
    { name: 'Other', value: (summary?.monthly_expense || 0) * 0.25 }
  ];

  // Line chart data for sales trend
  const salesTrendData = [
    { date: 'Mon', sales: (summary?.today_income || 0) * 0.6 },
    { date: 'Tue', sales: (summary?.today_income || 0) * 0.8 },
    { date: 'Wed', sales: (summary?.today_income || 0) * 1.2 },
    { date: 'Thu', sales: (summary?.today_income || 0) * 0.9 },
    { date: 'Fri', sales: (summary?.today_income || 0) * 1.5 },
    { date: 'Sat', sales: (summary?.today_income || 0) * 1.3 },
    { date: 'Sun', sales: (summary?.today_income || 0) * 1.1 }
  ];

  // Monthly profit trend
  const profitTrendData = [
    { month: 'Jan', profit: (summary?.monthly_income || 0) * 0.7 - (summary?.monthly_expense || 0) * 0.6 },
    { month: 'Feb', profit: (summary?.monthly_income || 0) * 0.8 - (summary?.monthly_expense || 0) * 0.65 },
    { month: 'Mar', profit: (summary?.monthly_income || 0) * 0.9 - (summary?.monthly_expense || 0) * 0.7 },
    { month: 'Apr', profit: (summary?.monthly_income || 0) * 1.1 - (summary?.monthly_expense || 0) * 0.75 },
    { month: 'May', profit: (summary?.monthly_income || 0) * 1.2 - (summary?.monthly_expense || 0) * 0.8 },
    { month: 'Jun', profit: (summary?.monthly_income || 0) - (summary?.monthly_expense || 0) },
  ];

  const colors = ['#22C55E', '#F59E0B', '#EF4444'];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
      gap: '24px',
      marginBottom: '40px'
    }}>
      {/* Income vs Expense Bar Chart */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.4)',
        borderRadius: '20px',
        padding: '28px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
        animation: 'slideUp 0.5s ease-out 0.2s both'
      }}>
        <h3 style={{
          margin: '0 0 24px 0',
          fontSize: '16px',
          fontWeight: 700,
          color: '#1F2937',
          fontFamily: 'Poppins, sans-serif'
        }}>
          {t('dashboard.incomeVsExpense')}
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={[
            { name: t('dashboard.thisMonth'), income: summary?.monthly_income || 0, expense: summary?.monthly_expense || 0 }
          ]}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(99, 102, 241, 0.1)" />
            <XAxis dataKey="name" stroke="#6B7280" />
            <YAxis stroke="#6B7280" />
            <Tooltip
              contentStyle={{
                background: 'rgba(31, 41, 55, 0.95)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '12px',
                color: 'white'
              }}
            />
            <Legend />
            <Bar dataKey="income" fill="#22C55E" radius={[8, 8, 0, 0]} />
            <Bar dataKey="expense" fill="#EF4444" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Monthly Profit Trend */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.4)',
        borderRadius: '20px',
        padding: '28px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
        animation: 'slideUp 0.5s ease-out 0.3s both'
      }}>
        <h3 style={{
          margin: '0 0 24px 0',
          fontSize: '16px',
          fontWeight: 700,
          color: '#1F2937',
          fontFamily: 'Poppins, sans-serif'
        }}>
          {t('dashboard.monthlyProfitTrend')}
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={profitTrendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(99, 102, 241, 0.1)" />
            <XAxis dataKey="month" stroke="#6B7280" />
            <YAxis stroke="#6B7280" />
            <Tooltip
              contentStyle={{
                background: 'rgba(31, 41, 55, 0.95)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '12px',
                color: 'white'
              }}
            />
            <Line
              type="monotone"
              dataKey="profit"
              stroke="#6366F1"
              strokeWidth={3}
              dot={{ fill: '#6366F1', r: 5 }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Expense Category Pie Chart */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.4)',
        borderRadius: '20px',
        padding: '28px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
        animation: 'slideUp 0.5s ease-out 0.4s both'
      }}>
        <h3 style={{
          margin: '0 0 24px 0',
          fontSize: '16px',
          fontWeight: 700,
          color: '#1F2937',
          fontFamily: 'Poppins, sans-serif'
        }}>
          {t('dashboard.expenseCategories')}
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={expenseData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {expenseData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                background: 'rgba(31, 41, 55, 0.95)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '12px',
                color: 'white'
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Sales Trend Line Chart */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.4)',
        borderRadius: '20px',
        padding: '28px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
        animation: 'slideUp 0.5s ease-out 0.5s both'
      }}>
        <h3 style={{
          margin: '0 0 24px 0',
          fontSize: '16px',
          fontWeight: 700,
          color: '#1F2937',
          fontFamily: 'Poppins, sans-serif'
        }}>
          Weekly Sales Trend
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={salesTrendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(99, 102, 241, 0.1)" />
            <XAxis dataKey="date" stroke="#6B7280" />
            <YAxis stroke="#6B7280" />
            <Tooltip
              contentStyle={{
                background: 'rgba(31, 41, 55, 0.95)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '12px',
                color: 'white'
              }}
            />
            <Line
              type="monotone"
              dataKey="sales"
              stroke="#F59E0B"
              strokeWidth={3}
              dot={{ fill: '#F59E0B', r: 5 }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
