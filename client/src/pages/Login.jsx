import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { Cross } from 'lucide-react';
import { validateEmail } from '../lib/utils';
import { Input } from '../components/ui/input';
import { useForm } from 'react-hook-form';

const Login = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [apiError, setApiError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    setApiError('');

    try {
      const response = await api.post('/auth/login', data);
      login(response.data);
      navigate('/');
    } catch (err) {
      setApiError(err.response?.data?.error || 'An error occurred during login. Please try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form 
        onSubmit={handleSubmit(onSubmit)} 
        className="flex flex-col w-full max-w-sm gap-4 p-8 bg-white border border-gray-200 rounded-lg shadow-md"
      >
        <div className="flex flex-col items-center justify-center mb-2">
          <Cross className="w-12 h-12 text-[#185FA5]" />
          <h1 className="mt-2 text-3xl font-bold text-gray-800">
            Med<span className="text-[#185FA5]">Portal</span>
          </h1>
          <p className="mt-1 text-sm font-medium text-gray-500">Clinical Patient Research Platform</p>
        </div>
        
        <hr className="w-full border-gray-200" />
        
        {apiError && <div className="text-sm text-center text-red-600">{apiError}</div>}
        
        <div className="flex flex-col">
          <label htmlFor="email" className="mb-1 text-sm font-medium text-gray-700">Email</label>
          <Input 
            id="email"
            type="email" 
            {...register('email', { 
              required: 'Email is required.', 
              validate: (val) => validateEmail(val) || 'Please enter a valid email address.' 
            })}
            className={errors.email ? 'border-red-500' : ''}
          />
          {errors.email && <span className="mt-1 text-xs text-red-600">{errors.email.message}</span>}
        </div>

        <div className="flex flex-col">
          <label htmlFor="password" className="mb-1 text-sm font-medium text-gray-700">Password</label>
          <Input 
            id="password"
            type="password" 
            {...register('password', { required: 'Password is required.' })}
            className={errors.password ? 'border-red-500' : ''}
          />
          {errors.password && <span className="mt-1 text-xs text-red-600">{errors.password.message}</span>}
        </div>

        <button type="submit" className="px-4 py-2 mt-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Login
        </button>

        <p className="text-sm text-center text-gray-600">
          Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;