# Laravel Project Example

## Project Structure
```
laravel-project/
├── app/
│   ├── Http/Controllers/
│   ├── Models/
│   ├── Services/
│   └── Providers/
├── config/
├── database/
│   ├── migrations/
│   └── seeders/
├── resources/
│   ├── views/
│   └── js/
├── routes/
│   ├── web.php
│   └── api.php
└── tests/
    ├── Feature/
    └── Unit/
```

## Development Workflow

1. Create migration and model
2. Define relationships
3. Create controller with resource methods
4. Define routes
5. Create views/API resources
6. Write tests
7. Run migration

## Example Implementation

### Model
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    protected $fillable = ['name', 'description', 'price'];
    
    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}
```

### Controller
```php
<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function index()
    {
        return Product::with('category')->paginate(15);
    }
    
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'description' => 'required|string',
            'price' => 'required|numeric|min:0'
        ]);
        
        return Product::create($validated);
    }
}
```

### Routes
```php
<?php

use App\Http\Controllers\ProductController;

Route::resource('products', ProductController::class);
```