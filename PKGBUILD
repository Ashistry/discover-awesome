# Maintainer: Your Name <your.email@example.com>
pkgname=my_project
pkgver=0.1
pkgrel=1
pkgdesc="A brief description of your project"
arch=('any')
url="https://github.com/Ashistry/discover-awesome"  # Replace with your project's URL
license=('MIT')  # Adjust according to your license
depends=('python' 'python-setuptools')  # List any dependencies here
source=("https://github.com/Ashistry/discover-awesome/archive/refs/tags/v${pkgver}.tar.gz")  # Adjust the source URL
sha256sums=('SKIP')  # You can generate this with `makepkg -g` after the first build

package() {
    cd "$srcdir/$pkgname-$pkgver"
    
    # Install the package using pip
    python setup.py install --root="$pkgdir" --optimize=1
}
