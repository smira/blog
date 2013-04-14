/* 

 Copyright 2005 Bob Ippolito <bob@redivi.com>  
 Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

*/

var Deferred = Class.create(
{
    initialize : function() {
            this.chain = [];
            this.fired = -1;
            this.paused = 0;
            this.results = [null, null];
            this.chained = false;
            this.__errorTimer = null;
        },

        /**
          The primitive that means either callback or errback
        */
        _resback: function (res) {
            this.fired = ((res instanceof Error) ? 1 : 0);
            this.results[this.fired] = res;
            this._fire();
        },

        _check: function () {
            if (this.fired != -1)
                throw new Error("Already fired");
        },

        callback: function (res) {
            this._check();
            if (res instanceof Deferred)
                throw new Error("Deferred instances can only be chained if they are the result of a callback");
            this._resback(res);
        },
        
        errback: function (res) {
            this._check();
           if (res instanceof Deferred)
               throw new Error("Deferred instances can only be chained if they are the result of a callback");
            if (!(res instanceof Error))
                res = new Error(res);
            this._resback(res);
        },

        addBoth: function (fn) {
            if (arguments.length != 1)
                throw new Error("No extra args supported");
            return this.addCallbacks(fn, fn);
        },

        addCallback: function (fn) {
            if (arguments.length != 1)
                throw new Error("No extra args supported");
            return this.addCallbacks(fn, null);
        },

        addErrback: function (fn) {
            if (arguments.length != 1)
                throw new Error("No extra args supported");
            return this.addCallbacks(null, fn);
        },

        addCallbacks: function (cb, eb) {
            if (this.chained) {
                throw new Error("Chained Deferreds can not be re-used");
            }
            this.chain.push([cb, eb]);
            if (this.fired >= 0) {
                this._fire();
            }
            return this;
        },

        /**
         *
         * Used internally to exhaust the callback sequence when a result
         * is available.
         */

        _fire: function () {
            var chain = this.chain;
            var fired = this.fired;
            var res = this.results[fired];
            var self = this;
            var cb = null;
            if (self.__errorTimer != null)
            {
                clearInterval(self.__errorTimer);
                self.__errorTimer = null;
            }
            while (chain.length > 0 && this.paused === 0) {
                // Array
                var pair = chain.shift();
                var f = pair[fired];
                if (f === null) {
                    continue;
                }
                try {
                    res = f(res);
                    fired = ((res instanceof Error) ? 1 : 0);
                    if (res instanceof Deferred) {
                        cb = function (res) {
                            self._resback(res);
                            self.paused--;
                            if ((self.paused === 0) && (self.fired >= 0)) {
                                self._fire();
                            }
                        };
                        this.paused++;
                    }
                } catch (err) {
                    fired = 1;
                    if (!(err instanceof Error)) {
                        err = new Error(err);
                    }
                    res = err;
                }
            }
            this.fired = fired;
            this.results[fired] = res;
            if (cb && this.paused) {
                // this is for "tail recursion" in case the dependent deferred
                // is already fired
                res.addBoth(cb);
                res.chained = true;
            }
            if (this.fired == 1)
            {
                self.__errorTimer = setInterval(function() { self.__reportError() }, 1000);
            }
        },
        __reportError : function()
            {
                console.error("Unhandled error in Deferred (possibly?):");
                console.error(this.results[this.fired]);
                clearInterval(this.__errorTimer);
                self.__errorTimer = null;
            }
});

Deferred.succeed = function(result) {
            var d = new Deferred();
            d.callback.apply(d, arguments);
            return d;
        };

Deferred.fail = function(result) {
            var d = new Deferred();
            d.errback.apply(d, arguments);
            return d;
        };
