import React from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { useLanguage } from '../hooks/useLanguage';

export default function ChartsSection({ summary }) {
  const { t, language } = useLanguage();
  
  const monthNames = language === 'ta' ? ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்'] : language === 'hi' ? ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const dayNames = language === 'ta' ? ['திங்கட்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி', 'ஞாயிறு'] : language === 'hi' ? ['सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि', 'रवि'] : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  
  // Pie chart data for expense categories
  const expenseData = [
    { name: t('dashboard.expenseCategories') + ' 1', value: (summary?.monthly_expense || 0) * 0.4 },
    { name: t('dashboard.expenseCategories') + ' 2', value: (summary?.monthly_expense || 0) * 0.35 },
    { name: t('common.categories.other'), value: (summary?.monthly_expense || 0) * 0.25 }
  ];

  // Line chart data for sales trend
  const salesTrendData = [
    { date: dayNames[0], sales: (summary?.today_income || 0) * 0.6 },
    { date: dayNames[1], sales: (summary?.today_income || 0) * 0.8 },
    { date: dayNames[2], sales: (summary?.today_income || 0) * 1.2 },
    { date: dayNames[3], sales: (summary?.today_income || 0) * 0.9 },
    { date: dayNames[4], sales: (summary?.today_income || 0) * 1.5 },
    { date: dayNames[5], sales: (summary?.today_income || 0) * 1.3 },
    { date: dayNames[6], sales: (summary?.today_income || 0) * 1.1 }
  ];

  // Monthly profit trend
  const profitTrendData = [
    { month: monthNames[0], profit: (summary?.monthly_income || 0) * 0.7 - (summary?.monthly_expense || 0) * 0.6 },
    { month: monthNames[1], profit: (summary?.monthly_income || 0) * 0.8 - (summary?.monthly_expense || 0) * 0.65 },
    { month: monthNames[2], profit: (summary?.monthly_income || 0) * 0.9 - (summary?.monthly_expense || 0) * 0.7 },
    { month: monthNames[3], profit: (summary?.monthly_income || 0) * 1.1 - (summary?.monthly_expense || 0) * 0.75 },
    { month: monthNames[4], profit: (summary?.monthly_income || 0) * 1.2 - (summary?.monthly_expense || 0) * 0.8 },
    { month: monthNames[5], profit: (summary?.monthly_income || 0) - (summary?.monthly_expense || 0) },
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
            <Bar dataKey="income" name={t('nav.income')} fill="#22C55E" radius={[8, 8, 0, 0]} />
            <Bar dataKey="expense" name={t('nav.expense')} fill="#EF4444" radius={[8, 8, 0, 0]} />
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
          {t('dashboard.monthlySales') || 'Weekly Sales Trend'}
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
