# React Project Example

## Project Structure
```
react-project/
├── src/
│   ├── components/
│   │   ├── common/
│   │   └── pages/
│   ├── hooks/
│   ├── services/
│   ├── utils/
│   ├── context/
│   └── styles/
├── public/
├── tests/
└── docs/
```

## Development Workflow

1. Plan component hierarchy
2. Create reusable components
3. Implement state management
4. Add API integration
5. Write tests
6. Optimize performance

## Example Implementation

### Component
```jsx
import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const { loading, error, fetchData } = useApi();

  useEffect(() => {
    const loadProducts = async () => {
      const data = await fetchData('/api/products');
      setProducts(data);
    };
    
    loadProducts();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="product-list">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};
```

### Custom Hook
```jsx
import { useState } from 'react';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async (url) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('API Error');
      return await response.json();
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, fetchData };
};
```

### Test Example
```jsx
import { render, screen, waitFor } from '@testing-library/react';
import { ProductList } from './ProductList';

test('renders product list', async () => {
  render(<ProductList />);
  
  await waitFor(() => {
    expect(screen.getByText('Product 1')).toBeInTheDocument();
  });
});
```